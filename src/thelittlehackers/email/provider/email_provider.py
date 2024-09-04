# MIT License
#
# Copyright (C) 2024 The Little Hackers.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import annotations

import abc
import pathlib
from typing import Iterable

from thelittlehackers.constant.email import FILE_EXTENSION_MIME_TYPE_MAP
from thelittlehackers.model.email import Email


class EmailServiceBase(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @staticmethod
    def _find_file_extension_mime_type(
            file_name: str,
            strict: bool = False
    ) -> str | None:
        """
        Determine the MIME type based on the file extension.

        This method returns the MIME (Multipurpose Internet Mail Extensions)
        type associated with the file extension of the given file name.  MIME
        types are used to describe the nature and format of a file or byte
        stream and are standardized by the IETF in RFC 6838.


        :param file_name: The name of the file for which the MIME type is to
            be determined.

        :param strict: If set to ``True``, raises a ``ValueError`` if the MIME
            type cannot be determined.  If ``False``, the method returns ``None``
             when the MIME type is not found.


        :return: The MIME type as a string if the file extension is recognized,
            otherwise ``None``.


        :raises ValueError: If ``strict`` is ``True`` and the MIME type cannot
            be found.
        """
        file_extension = pathlib.Path(file_name).suffix
        mime_type = FILE_EXTENSION_MIME_TYPE_MAP.get(file_extension)

        if not file_extension and strict:
            raise ValueError(
                f"The MIME type of the file extension '{file_extension}' has not been found"
            )

        return mime_type

    @staticmethod
    def _validate_emails(emails: Email | Iterable[Email]) -> Iterable[Email]:
        """
        Validate and normalize the input email(s).


        :param emails: A single ``Email`` instance or an iterable of ``Email` `
            instances to be validated.


        :return: An iterable containing one or more valid ``Email`` instances.


        :raises ValueError: If any element in the input is not an instance of
            ``Email``.
        """
        if isinstance(emails, Email):
            return [emails]


        if not isinstance(emails, Iterable) \
           or any(not isinstance(email, Email) for email in emails):
            raise ValueError(
                f"Argument 'emails' MUST be an instance of '{Email.__name__}' or an "
                f"iterable of '{Email.__name__}'"
            )

        return emails

    @abc.abstractmethod
    def send_emails(self, emails: Email | Iterable[Email]) -> None:
        """
        Send one or more emails.

        This abstract method is responsible for sending email messages.
        Subclasses must implement this method to define how the emails are
        sent, whether individually or in bulk.


        :param emails: A single ``Email`` instance or an iterable of ``Email` `
            instances to be sent.


        :raises NotImplementedError: This method must be implemented by
            subclasses.
        """
        raise NotImplementedError()
