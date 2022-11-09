from airflow.utils.context import Context
from airflow.operators.bash import BashOperator
from airflow.lineage import apply_lineage, prepare_lineage


class AerofoilBashOperator(BashOperator):
    def __init__(self, *, bash_context={}, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bash_context = bash_context

    def execute(self, context: Context):
        context["bash_context"] = self.bash_context
        super().execute(context)
