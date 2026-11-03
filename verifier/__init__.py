from contract import Task, Tool

from .calculate import result, verify_submission


def verify_input(tool, value):
    Tool(tool)
    return result(True, "Acknowledgement request is valid.")


def verify_output(tool, input_value, output_value, workspace):
    Tool(tool)
    valid = output_value.acknowledged
    return result(valid, "Acknowledged." if valid else "Expected a fixed acknowledgement.")


def verify_task(task, arguments, output, reference, workspace):
    Task(task)
    return verify_submission(arguments, output)
