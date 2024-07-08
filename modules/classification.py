import numpy as np
from sklearn.cross_decomposition import CCA
from sklearn.linear_model import LogisticRegression

class CCAModel:
    def __init__(self, n_components=2):
        self.n_components = n_components
        self.cca = CCA(n_components=self.n_components)
        self.classifier = LogisticRegression()

    def fit(self, X, Y):
        """
        Fits the CCA model and the classifier.

        X: numpy array of shape (n_samples, n_features)
        Y: numpy array of shape (n_samples,)
        """
        # Perform CCA
        self.cca.fit(X, Y)

        # Transform X to CCA space
        X_cca, _ = self.cca.transform(X, Y)

        # Fit the classifier on the transformed data
        self.classifier.fit(X_cca, Y)

    def predict(self, X):
        """
        Predicts the class labels for the given data.

        X: numpy array of shape (n_samples, n_features)

        Returns: numpy array of shape (n_samples,)
        """
        # Transform X to CCA space
        X_cca = self.cca.transform(X)

        # Predict class labels
        return self.classifier.predict(X_cca)

    def predict_proba(self, X):
        """
        Predicts class probabilities for the given data.

        X: numpy array of shape (n_samples, n_features)

        Returns: numpy array of shape (n_samples, n_classes)
        """
        # Transform X to CCA space
        X_cca = self.cca.transform(X)

        # Predict class probabilities
        return self.classifier.predict_proba(X_cca)
