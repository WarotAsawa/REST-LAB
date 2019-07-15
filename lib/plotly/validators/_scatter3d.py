import _plotly_utils.basevalidators


class Scatter3dValidator(_plotly_utils.basevalidators.CompoundValidator):

    def __init__(self, plotly_name='scatter3d', parent_name='', **kwargs):
        super(Scatter3dValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop('data_class_str', 'Scatter3d'),
            data_docs=kwargs.pop(
                'data_docs', """
            connectgaps
                Determines whether or not gaps (i.e. {nan} or
                missing values) in the provided data arrays are
                connected.
            customdata
                Assigns extra data each datum. This may be
                useful when listening to hover, click and
                selection events. Note that, "scatter" traces
                also appends customdata items in the markers
                DOM elements
            customdatasrc
                Sets the source reference on plot.ly for
                customdata .
            error_x
                plotly.graph_objs.scatter3d.ErrorX instance or
                dict with compatible properties
            error_y
                plotly.graph_objs.scatter3d.ErrorY instance or
                dict with compatible properties
            error_z
                plotly.graph_objs.scatter3d.ErrorZ instance or
                dict with compatible properties
            hoverinfo
                Determines which trace information appear on
                hover. If `none` or `skip` are set, no
                information is displayed upon hovering. But, if
                `none` is set, click and hover events are still
                fired.
            hoverinfosrc
                Sets the source reference on plot.ly for
                hoverinfo .
            hoverlabel
                plotly.graph_objs.scatter3d.Hoverlabel instance
                or dict with compatible properties
            hovertemplate
                Template string used for rendering the
                information that appear on hover box. Note that
                this will override `hoverinfo`. Variables are
                inserted using %{variable}, for example "y:
                %{y}". Numbers are formatted using d3-format's
                syntax %{variable:d3-format}, for example
                "Price: %{y:$.2f}". See https://github.com/d3/d
                3-format/blob/master/README.md#locale_format
                for details on the formatting syntax. The
                variables available in `hovertemplate` are the
                ones emitted as event data described at this
                link https://plot.ly/javascript/plotlyjs-
                events/#event-data. Additionally, every
                attributes that can be specified per-point (the
                ones that are `arrayOk: true`) are available.
                Anything contained in tag `<extra>` is
                displayed in the secondary box, for example
                "<extra>{fullData.name}</extra>".
            hovertemplatesrc
                Sets the source reference on plot.ly for
                hovertemplate .
            hovertext
                Sets text elements associated with each (x,y,z)
                triplet. If a single string, the same string
                appears over all the data points. If an array
                of string, the items are mapped in order to the
                this trace's (x,y,z) coordinates. To be seen,
                trace `hoverinfo` must contain a "text" flag.
            hovertextsrc
                Sets the source reference on plot.ly for
                hovertext .
            ids
                Assigns id labels to each datum. These ids for
                object constancy of data points during
                animation. Should be an array of strings, not
                numbers or any other type.
            idssrc
                Sets the source reference on plot.ly for  ids .
            legendgroup
                Sets the legend group for this trace. Traces
                part of the same legend group hide/show at the
                same time when toggling legend items.
            line
                plotly.graph_objs.scatter3d.Line instance or
                dict with compatible properties
            marker
                plotly.graph_objs.scatter3d.Marker instance or
                dict with compatible properties
            mode
                Determines the drawing mode for this scatter
                trace. If the provided `mode` includes "text"
                then the `text` elements appear at the
                coordinates. Otherwise, the `text` elements
                appear on hover. If there are less than 20
                points and the trace is not stacked then the
                default is "lines+markers". Otherwise, "lines".
            name
                Sets the trace name. The trace name appear as
                the legend item and on hover.
            opacity
                Sets the opacity of the trace.
            projection
                plotly.graph_objs.scatter3d.Projection instance
                or dict with compatible properties
            scene
                Sets a reference between this trace's 3D
                coordinate system and a 3D scene. If "scene"
                (the default value), the (x,y,z) coordinates
                refer to `layout.scene`. If "scene2", the
                (x,y,z) coordinates refer to `layout.scene2`,
                and so on.
            selectedpoints
                Array containing integer indices of selected
                points. Has an effect only for traces that
                support selections. Note that an empty array
                means an empty selection where the `unselected`
                are turned on for all points, whereas, any
                other non-array values means no selection all
                where the `selected` and `unselected` styles
                have no effect.
            showlegend
                Determines whether or not an item corresponding
                to this trace is shown in the legend.
            stream
                plotly.graph_objs.scatter3d.Stream instance or
                dict with compatible properties
            surfaceaxis
                If "-1", the scatter points are not fill with a
                surface If 0, 1, 2, the scatter points are
                filled with a Delaunay surface about the x, y,
                z respectively.
            surfacecolor
                Sets the surface fill color.
            text
                Sets text elements associated with each (x,y,z)
                triplet. If a single string, the same string
                appears over all the data points. If an array
                of string, the items are mapped in order to the
                this trace's (x,y,z) coordinates. If trace
                `hoverinfo` contains a "text" flag and
                "hovertext" is not set, these elements will be
                seen in the hover labels.
            textfont
                plotly.graph_objs.scatter3d.Textfont instance
                or dict with compatible properties
            textposition
                Sets the positions of the `text` elements with
                respects to the (x,y) coordinates.
            textpositionsrc
                Sets the source reference on plot.ly for
                textposition .
            textsrc
                Sets the source reference on plot.ly for  text
                .
            uid
                Assign an id to this trace, Use this to provide
                object constancy between traces during
                animations and transitions.
            uirevision
                Controls persistence of some user-driven
                changes to the trace: `constraintrange` in
                `parcoords` traces, as well as some `editable:
                true` modifications such as `name` and
                `colorbar.title`. Defaults to
                `layout.uirevision`. Note that other user-
                driven trace attribute changes are controlled
                by `layout` attributes: `trace.visible` is
                controlled by `layout.legend.uirevision`,
                `selectedpoints` is controlled by
                `layout.selectionrevision`, and
                `colorbar.(x|y)` (accessible with `config:
                {editable: true}`) is controlled by
                `layout.editrevision`. Trace changes are
                tracked by `uid`, which only falls back on
                trace index if no `uid` is provided. So if your
                app can add/remove traces before the end of the
                `data` array, such that the same trace has a
                different index, you can still preserve user-
                driven changes if you give each trace a `uid`
                that stays with it as it moves.
            visible
                Determines whether or not this trace is
                visible. If "legendonly", the trace is not
                drawn, but can appear as a legend item
                (provided that the legend itself is visible).
            x
                Sets the x coordinates.
            xcalendar
                Sets the calendar system to use with `x` date
                data.
            xsrc
                Sets the source reference on plot.ly for  x .
            y
                Sets the y coordinates.
            ycalendar
                Sets the calendar system to use with `y` date
                data.
            ysrc
                Sets the source reference on plot.ly for  y .
            z
                Sets the z coordinates.
            zcalendar
                Sets the calendar system to use with `z` date
                data.
            zsrc
                Sets the source reference on plot.ly for  z .
"""
            ),
            **kwargs
        )
