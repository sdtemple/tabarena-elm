from autogluon.common.space import Real, Categorical

from tabarena.benchmark.models.ag.gfdl_torch.gfdl_torch import ELMTorch, RVFLTorch

from ...utils.config_utils import ConfigGenerator


search_space = {
        "hidden_layer_sizes": Categorical(
            [100,], [200,], [400,], 
            [100, 100], [200, 200], [400, 400],
            [100, 100, 100], [200, 200, 200],
            [400, 400, 400, 400, 400],
            
        ),
        "activation": Categorical(
            "identity",
            "tanh",
            "relu",
            "sigmoid",
            "softmax",
            "softmin",
            "log_sigmoid",
            "log_softmax",
        ),
        "weight_scheme": Categorical(
            "zeros",
            "uniform",
            "normal",
            "he_uniform",
            "lecun_uniform",
            "glorot_uniform",
            "he_normal",
            "lecun_normal",
            "glorot_normal",
        ),
        "reg_alpha": Real(1e-10, 100.0, default=None, log=True),
    }

manual_configs = [{}]


gen_elm = ConfigGenerator(
    model_cls=ELMTorch,
    manual_configs=manual_configs,
    search_space=search_space,
)


def generate_configs_elm(num_random_configs=200):
    config_generator = ConfigGenerator(
        name="ELMTorch",
        manual_configs=manual_configs,
        search_space=search_space,
    )

    return config_generator.generate_all_configs(
        num_random_configs=num_random_configs
    )

gen_rvfl = ConfigGenerator(
    model_cls=RVFLTorch,
    manual_configs=manual_configs,
    search_space=search_space,
)


def generate_configs_rvfl(num_random_configs=200):
    config_generator = ConfigGenerator(
        name="RVFLTorch",
        manual_configs=manual_configs,
        search_space=search_space,
    )

    return config_generator.generate_all_configs(
        num_random_configs=num_random_configs
    )