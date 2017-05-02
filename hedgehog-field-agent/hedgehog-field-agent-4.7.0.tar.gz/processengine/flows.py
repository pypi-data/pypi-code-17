from viewflow import frontend, flow
from viewflow.base import Flow, this
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from processengine import models, views
from processengine.models import AlertProcess


@frontend.register
class AlertFlow(Flow):
    process_class = AlertProcess

    start = (flow
             .Start(CreateProcessView, fields=["text"])
             .Permission(auto_create=True)
             .Next(this.approve))

    approve = (flow
               .View(UpdateProcessView, fields=["approved"])
               .Permission(auto_create=True)
               .Next(this.check_approve))

    check_approve = (flow
                     .If(lambda activation: activation.process.approved)
                     .Then(this.send)
                     .Else(this.end))

    send = (flow
            .Handler(this.send_notifcation_request)
            .Next(this.end))

    end = flow.End()

    def send_notifcation_request(self, activation):
        print(activation.process.text)




@frontend.register
class AssetOutputFlow(Flow):
    process_class = models.ObserverProcess

    first_parameter_setup = flow.Start(
        views.TaskDashboardView
    ).Next(this.show_output)

    second_parameter_setup = flow.Start(
        views.additional_parameter_set
    ).Next(this.show_output)

    show_output = flow.View(
        views.task_data
    ).Next(this.split_analysis)

    split_analysis = (
        flow.Split()
        .Next(
            this.change_parameters,
            cond=lambda act: act.process.change_parameters_required
        ).Next(
            this.engine_tick,
            cond=lambda act: act.process.engine_tick_required
        ).Next(
            this.join_analysis
        )
    )

    change_parameters = flow.View(
        views.TaskDashboardView
    ).Next(this.join_analysis)

    engine_tick = flow.View(
        views.TaskDashboardView
    ).Next(this.join_analysis)

    # tumor_markers_test = flow.View(
    #     views.GenericTestFormView,
    #     model=models.TumorMarkers,
    #     fields=[
    #         'alpha_fetoprotein', 'beta_gonadotropin', 'ca19',
    #         'cea', 'pap', 'pas'
    #     ],
    #     task_description='Tumor Markers Test'
    # ).Next(this.join_analysis)

    join_analysis = flow.Join().Next(this.end)

    end = flow.End()
