# Tracescopio: Simplifying Stack Trace Retrieval for Your Django Applications Remotely

Tracescopio is a simple Django app to get Python app's stack traces remotly.

It runs as every Django app:

    git clone https://github.com/t3rcio/tracescopio
    cd tracescopio
    pip install -r requirements.txt
    ./manage.py runserver 0.0.0.0:8000

To capture the stack traces use the [Tracescopio python package](https://pypi.org/project/tracescopio/)