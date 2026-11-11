from autogluon.common.space import Real, Categorical

from tabarena.benchmark.models.ag.sklearn_elm_pr.sklearn_elm_pr import ELMPR, RVFLPR

from ...utils.config_utils import ConfigGenerator

widths = [2**7, 2**8, 2**9, 2**10]
depths = [2**0, 2**1, 2**2, 2**3]

hidden_layer_sizes = [
    [width] * depth
    for depth in depths
    for width in widths
]

search_space = {
        "hidden_layer_sizes": Categorical(
            *hidden_layer_sizes
            # [100,], [200,], [400,], 
            # [100, 100], [200, 200], [400, 400],
            # [100, 100, 100], [200, 200, 200],
            # [400, 400, 400, 400, 400],
        ),
        "activation": Categorical(
            # "identity",
            "tanh",
            "relu",
            "logistic",
            # "softmax",
            # "softmin",
            "log_sigmoid",
            # "log_softmax",
        ),
        "weight_init": Categorical(
            # "zeros",
            # "uniform",
            # "normal",
            # "he_uniform",
            "lecun_uniform",
            # "glorot_uniform",
            # "he_normal",
            "lecun_normal",
            # "glorot_normal",
        ),
        "ridge_alpha": Real(1e-10, 100.0, default=None, log=True),
    }

manual_configs = [{}]


gen_elm = ConfigGenerator(
    model_cls=ELMPR,
    manual_configs=manual_configs,
    search_space=search_space,
)


def generate_configs_elm(num_random_configs=200):
    config_generator = ConfigGenerator(
        name="ELMPR",
        manual_configs=manual_configs,
        search_space=search_space,
    )

    return config_generator.generate_all_configs(
        num_random_configs=num_random_configs
    )

gen_rvfl = ConfigGenerator(
    model_cls=RVFLPR,
    manual_configs=manual_configs,
    search_space=search_space,
)


def generate_configs_rvfl(num_random_configs=200):
    config_generator = ConfigGenerator(
        name="RVFLPR",
        manual_configs=manual_configs,
        search_space=search_space,
    )

    return config_generator.generate_all_configs(
        num_random_configs=num_random_configs
    )