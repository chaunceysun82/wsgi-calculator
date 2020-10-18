"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback

def guide(*args):
    instruction_text = """How to use this page:
1. http://localhost:8080/ followed by operators and two numbers spaced by /.
2. Return the operation results.
3. The operators include add, substract, multiply and divide.
4. The numbers must be integer or float.
5. Examples: http://localhost:8080/multiply/3/5 will return 15."""
    instruction = instruction_text.split('\n')

    body_text = '<h1>{}</h1>'.format(instruction[0])
    body = [body_text, '<ul>']
    item_template = '<li>{}</li>'
    for item in instruction[1:]:
        body.append(item_template.format(item))
    body.append('</ul>')

    return '\n'.join(body)

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    res = int(args[0]) + int(args[1])
    body = "<h>{} adds {} equals {}</h>".format(args[0], args[1], res)

    return body

def substract(*args):
    res = int(args[0])-int(args[1])
    body = "<h>{} substracts {} equals {}</h>".format(args[0], args[1], res)

    return body

def multiply(*args):
    res = int(args[0]) * int(args[1])
    body = "<h>{} multiplies {} equals {}</h>".format(args[0], args[1], res)

    return body

def divide(*args):
    res = int(args[0]) / int(args[1])
    body = "<h>{} divided by {} equals {}</h>".format(args[0], args[1], res)

    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {'': guide,
             'add': add,
             'substract': substract,
             'multiply': multiply,
             'divide': divide,
            }
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):

    import pprint
    pprint.pprint(environ)

    status = "200 OK"
    headers = [('Content-type', 'text/html')]

    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h>Not Found</h1>"
    except ZeroDivisionError:
        status = "200 OK"
        body = "<h>Can not divided by 0</h>"
    except Exception:
        status = "500"
        body = "<h>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
    # args = [3, 5]
    # a = divide(*args)
    # print(a)