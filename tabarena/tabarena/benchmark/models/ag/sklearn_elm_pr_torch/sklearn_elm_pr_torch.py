from __future__ import annotations

import numpy as np

from autogluon.core.models import AbstractModel
from autogluon.features.generators import LabelEncoderFeatureGenerator
from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import ExtremeLearningClassifier, ExtremeLearningRegressor
import torch

from typing import TYPE_CHECKING

from sklearn import config_context

if TYPE_CHECKING:
    import pandas as pd


class ELMPRTorchBase(AbstractModel):
    """Minimal implementation of a GFDL compatible with the scikit-learn API.
    For more details on how to implement an abstract model, see https://auto.gluon.ai/stable/tutorials/tabular/advanced/tabular-custom-model.html
    and compare to implementations of models under tabarena.benchmark/models/ag/.

    ELM and RVFL inherit from this
    """

    ag_key = "elm_pr_torch_base"
    ag_name = "ELMPRTorchBase"

    _supported_problem_types = ["regression",
                                "multiclass",
                                "binary"]

    direct_links: bool | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._feature_generator = None
        self.sc = None

    def _preprocess(self, X: pd.DataFrame, is_train=False, **kwargs) -> np.ndarray:
        """Model-specific preprocessing of the input data."""
        X = super()._preprocess(X, **kwargs)
        if is_train:
            self._feature_generator = LabelEncoderFeatureGenerator(verbosity=0)
            self._feature_generator.fit(X=X)
        if self._feature_generator.features_in:
            X = X.copy()
            X[self._feature_generator.features_in] = self._feature_generator.transform(X=X)

        X = X.fillna(-1).to_numpy(dtype=np.float32)

        if is_train:
            self.sc = StandardScaler().fit(X)

        X = self.sc.transform(X)
        X = torch.from_numpy(X)
        return X

    def _fit(
        self,
        X: pd.DataFrame,  # training data
        y: pd.Series,  # training labels
        # X_val=None,  # val data
        # y_val=None,  # val labels
        # time_limit=None,  # time limit in seconds (ignored in tutorial)
        num_cpus: int = 1,  # number of CPUs to use for training
        # num_gpus: int = 0,  # number of GPUs to use for training
        **kwargs,  # kwargs includes many other potential inputs, refer to AbstractModel documentation for details
    ):
    
        if self.problem_type == "regression":

            model_cls = ExtremeLearningRegressor
        else:

            # case for 'binary' and 'multiclass',
            model_cls = ExtremeLearningClassifier

        X = self._preprocess(X, is_train=True)
        y_np = y.to_numpy(copy=False)
        params = self._get_model_params()
        
        params["direct_links"] = self.direct_links

        self.model = model_cls(**params)
        with config_context(array_api_dispatch=True):
            self.model.fit(X, y_np)

    def _predict(self, X: pd.DataFrame, **kwargs) -> np.ndarray:
        """Preprocesses test data, converts to torch tensors, and outputs NumPy predictions."""
        X = self._preprocess(X, is_train=False, **kwargs)

        with config_context(array_api_dispatch=True):
            preds = self.model.predict(X)

        if isinstance(preds, torch.Tensor):
            return preds.detach().cpu().numpy()
        return np.asarray(preds)

    def _predict_proba(self, X: pd.DataFrame, **kwargs) -> np.ndarray:
        X = self._preprocess(X, is_train=False, **kwargs)

        with config_context(array_api_dispatch=True):
            if self.problem_type == "regression":
                preds = self.model.predict(X)
            else:
                preds = self.model.predict_proba(X)

        if isinstance(preds, torch.Tensor):
            preds = preds.detach().cpu().numpy()
        else:
            preds = np.asarray(preds)

        # this line is important!
        # when you override the _predict_proba from the AbstractModel
        # you can result in a shape output that doesn't align
        # with the autogluon customized AUROC function.
        # you get a rather uninformative error about there only being
        # one class, which is not the actual error.
        if self.problem_type != "regression":
            preds = self._convert_proba_to_unified_form(preds)
        return preds

    def _set_default_params(self):
        """Default parameters for the model."""
        default_params = {
            "hidden_layer_sizes": (100,),
            "activation": "identity",
            "weight_init": "uniform",
            "direct_links": False,
            "random_state": self.model_random_seed if hasattr(self, "model_random_seed") else 0,
            "ridge_alpha": 0.1,
            "rtol": None,
        }
        for param, val in default_params.items():
            self._set_default_param_value(param, val)

    def _get_default_auxiliary_params(self) -> dict:
        """Specifics allowed input data and that all other dtypes should be handled
        by the model-agnostic preprocessor.
        """
        default_auxiliary_params = super()._get_default_auxiliary_params()
        extra_auxiliary_params = {
            "valid_raw_types": ["int", "float", "category"],
        }
        default_auxiliary_params.update(extra_auxiliary_params)
        return default_auxiliary_params
    
    # @classmethod
    # def supported_problem_types(cls) -> list[str] | None:
    #     return ["binary", "multiclass", "regression"]


class ELMPRTorch(ELMPRTorchBase):
    """Extreme Learning Machine"""

    ag_key = "elm_pr_torch"
    ag_name = "ELMPRTorch"

    direct_links = False


class RVFLPRTorch(ELMPRTorchBase):
    """Random Vector Functional Link network"""

    ag_key = "rvfl_pr_torch"
    ag_name = "RVFLPRTorch"

    direct_links = True