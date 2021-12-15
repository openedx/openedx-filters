"""
Utilities for Open edX filters usage.
"""


class SensitiveDataManagementMixin:
    """
    Custom class used manage sensitive data within filter arguments.
    """

    sensitive_form_data = []

    @classmethod
    def extract_sensitive_data(cls, form_data):
        """
        Extract sensitive data from its child class input arguments.

        Example usage:

            >> sensitive_form_data = ["password"] # Specified in FilterExample
            >> form_data = {"username": "example", "password": "password"}
            >> sensitive_data = FilterExample.extract_sensitive_data(form_data)
            >> sensitive_data
            {"password": "password"}
            >> form_data
            {"username": "example"}
        """
        sensitive_data = {}
        base_form_data = form_data.copy()
        for key, value in base_form_data.items():
            if key in cls.sensitive_form_data:
                form_data.pop(key)
                sensitive_data[key] = value

        return sensitive_data
