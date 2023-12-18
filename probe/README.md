Tracescopio: Simplifying Stack Trace Retrieval for Your Django Applications Remotely

Tracescopio is a tool designed to make obtaining stack traces from your python app easy: the events are sent to your Tracescopio app. (You can install Tracescopio app in your own server. [See more.](https://github.com/t3rcio/tracescopio))

## Get started
Firts of all, make sure your have your own server running.
After that, use the pip command to install the tracescopio in your app:

    pip install tracescopio

Put the the your Tracescopio url server in your project's settings.py file:

    (...)
    TRACERSCOPIO_SERVER = '<your tracescopio-app url>'

Obtain the IDE code for your app:

    python manage.py shell
    from tracescopio import scopio
    TracescopioApp.new(name='foo', url='foo.com')
    {'ide':some-code-for-your-app', 'msg':'Success'}

Put the "ide" code in your project's settings.py file:

	(...)
    APP_TRACESCOPIO_IDE = '<the ide code for you app>'

Finally, to get the stack traces you can use the decorator or the middleware.

Decorator
--
Add the import

    (..)
    from tracescopio.decorators import traceme

Add the decorator

    @trace
    def the_view_raising_some_exception(request, *args, **kwargs):
        (...)

Middleware
--
In your settgins.py's middleware section, add the tracescopio middleware:

    (...)
    MIDDLEWARE = [
    	(...)
        "tracescopio.middleware.telemetria.TelemetryMiddleware",
    ]

That is it!