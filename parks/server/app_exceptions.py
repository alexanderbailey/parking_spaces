import fastapi.exceptions
import sqlalchemy.exc
from sqlalchemy.exc import *
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from parks.schemas.exceptions.base import PGExceptionModel, ExceptionModel
from .http_lookup_codes import pgcode_lookups, sqlalchemy_error_lookup
from .app import app


"""
Thinking we possibly should redo this to catch only the SQLAlchemyError base, then do a pycog2.errors.lookup 
and a giant switch statement that we can then return the exact code/error from one place. 
We can then just add new instances of errors to the list as and when we com across them.
Hopefully this should be more robust at catching any api errors that come about, at the moment there doesnt seem to be
a good way for sqlmodel to work with the rls and unique constraint errors that come aboutin general use.
This would also then allow us to take out all the try/catch stuff that is in some of the endpoints.

This all comes from the issue where sqlalchemy and sqlmodel dont allow nice access to the base exceptions for adding to 
the exception_handler property in the app

How does this then tie into the error handling in the front end, pgcode/pgerror?

IF YOU GET "ERROR CAUGHT, BUT RESPONSE ALREADY STARTED" REMOVE THE TRY CATCH FROM THE ENDPOINT AND TRY AGAIN

else return something broke default error message

Codes to work with:
    400: -
    401: unauthorised
    403: forbidden
    404: not found
    409: duplicate on unique
    422: Unprocessable content (malformed payload)
    
    500: internal server error

"""


@app.exception_handler(SQLAlchemyError)
@app.exception_handler(fastapi.exceptions.FastAPIError)
def default_handle_sqlalchemy_error(request: Request, exc) -> JSONResponse:
    """
    Global excpetion hanlder for the app. This should catch application layer errors that you would expect to happen and
    shoulud not handle exceptions that are caused by invalid codel. Any response around bad incoming data should have
    a suggested fix as part of the returned message

    Args:
        request:
        exc:

    Returns:
        JSON response containing the status code and the error message

    """
    try:
        # Is this a postgres error?
        try:
            exception = PGExceptionModel(
                pgcode=int(exc.orig.pgcode), pgerror=exc.orig.pgerror
            )
            # the statuc code lookup will fail for the errors we want to push to the next level of exception handling
            return JSONResponse(
                status_code=pgcode_lookups[exc.orig.pgcode],
                content=dict(exception),
            )
        # Otherwise, code lookup fails, try SQLAlchemy error
        except:
            exception = ExceptionModel(
                message=f"{sqlalchemy_error_lookup[type(exc).__name__]}",
                detail=f"{exc.with_traceback(exc.__traceback__)}",
                error=f"{type(exc).__name__}")
            return JSONResponse(
                status_code=sqlalchemy_error_lookup[type(exc).__name__],
                content=dict(exception)
            )
    # Otherwise, not an SQLAlchemy error, or not in the lookup table
    except Exception as e:
        exception = ExceptionModel(
            message=f"{type(exc)} is not an SQLAlchemy error, or not handled in the sqlalchemy exception list",
            detail=f"{exc.with_traceback(exc.__traceback__)}",
            error=f"Handling {type(exc)} caused the following error: {e=}"
        )

        return JSONResponse(
            status_code=500,
            content=dict(exception))
