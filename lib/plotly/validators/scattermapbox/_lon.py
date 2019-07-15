import _plotly_utils.basevalidators


class LonValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(
        self, plotly_name='lon', parent_name='scattermapbox', **kwargs
    ):
        super(LonValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'calc'),
            role=kwargs.pop('role', 'data'),
            **kwargs
        )
