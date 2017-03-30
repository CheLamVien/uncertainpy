
class GeneralFeatures(object):
    def __init__(self,
                 features_to_run="all",
                 new_utility_methods=None,
                 adaptive_features=None):

        # self.implemented_features = []
        self.utility_methods = ["calculateFeature",
                                "calculateFeatures",
                                "calculateAllFeatures",
                                "__init__",
                                "implementedFeatures",
                                "setup"]

        if new_utility_methods is None:
            new_utility_methods = []

        self.t = None
        self.U = None

        self._features_to_run = None
        self._adaptive_features = None

        self.utility_methods += new_utility_methods

        self.features_to_run = features_to_run
        self.adaptive_features = adaptive_features

    def setup(self):
        pass


    # @property
    # def t(self):
    #     return self._t
    #
    # @property
    # def U(self):
    #     return self._U

    @property
    def features_to_run(self):
        return self._features_to_run

    @features_to_run.setter
    def features_to_run(self, new_features_to_run):
        if new_features_to_run == "all":
            self._features_to_run = self.implementedFeatures()
        elif new_features_to_run is None:
            self._features_to_run = []
        elif isinstance(new_features_to_run, str):
            self._features_to_run = [new_features_to_run]
        else:
            self._features_to_run = new_features_to_run




    @property
    def adaptive_features(self):
        return self._adaptive_features


    @adaptive_features.setter
    def adaptive_features(self, new_adaptive_features):
        if new_adaptive_features == "all":
            self._adaptive_features = self.implementedFeatures()
        elif new_adaptive_features is None:
            self._adaptive_features = []
        elif isinstance(new_adaptive_features, str):
            self._adaptive_features = [new_adaptive_features]
        else:
            self._adaptive_features = new_adaptive_features



    def calculateFeature(self, feature_name):
        if feature_name in self.utility_methods:
            raise TypeError("%s is a utility method")

        # if not callable(getattr(self, feature_name)):
        #     raise NotImplementedError("%s is not a implemented feature" % (feature_name))

        return getattr(self, feature_name)()



    def calculateFeatures(self):
        results = {}
        for feature in self.features_to_run:
            feature_result = self.calculateFeature(feature)

            try:
                results[feature] = {"t": feature_result[0],
                                    "U": feature_result[1]}

                if len(feature_result) != 2:
                    raise ValueError

            except ValueError as error:
                msg = "feature_ {} must return t and U (return t, U | return None, U)".format(feature)
                if not error.args:
                    error.args = ("",)
                error.args = error.args + (msg,)
                raise

        return results


    def calculateAllFeatures(self):
        results = {}
        for feature in self.implementedFeatures():
            feature_result = self.calculateFeature(feature)

            try:
                results[feature] = {"t": feature_result[0],
                                    "U": feature_result[1]}

                if len(feature_result) != 2:
                    raise ValueError

            except ValueError as error:
                msg = "feature_ {} must return t and U (return t, U | return None, U)".format(feature)
                if not error.args:
                    error.args = ("",)
                error.args = error.args + (msg,)
                raise

        return results


    def implementedFeatures(self):
        """
        Return a list of all callable methods in feature
        """
        return [method for method in dir(self) if callable(getattr(self, method)) and method not in self.utility_methods and method not in dir(object)]
