__VERSION__ = '0.0.0'


from . import nicolive


__all__ = [
  'nicolive',
  'guess_service',
]


from urllib.parse import urlparse
from typing import Optional, Literal
from dataclasses import dataclass


"""
  Public APIs
"""


default_application_useragent = \
  'live_info_api_client_py/0.1.0+dev ' \
  '(+https://github.com/aoirint/live_info_api_client_py)'

default_useragent = 'facebookexternalhit/1.1;Googlebot/2.1' \
            f';{default_application_useragent}'


@dataclass
class GetLiveProgramData:
  name: Optional[str]
  description: Optional[str]
  url: Optional[str]
  thumbnail_url: Optional[str]
  start_date: Optional[str]  # ISO8601 timezone-aware datetime string
  end_date: Optional[str]  # ISO8601 timezone-aware datetime string


class GetLiveProgramError(Exception):
  pass


def get_live_program(
  live_id_or_url: str,
  service: Optional[str],
  useragent: str = default_useragent,
):
  if service is None:
    service = guess_service(live_id_or_url=live_id_or_url)

  if service is None:
    raise GetLiveProgramError(
      'Service not specified and auto selection failed. '
      'Specify an argument: --service=[nicolive]'
    )

  if service == 'nicolive':
    nicolive_program_result = \
      nicolive.get_nicolive_program(
        live_id_or_url=live_id_or_url,
        useragent=useragent,
      )

    if nicolive_program_result.result_type == 'success':
      if nicolive_program_result.data_type == 'nicolive_program':
        print(nicolive_program_result.data)
      else:
        raise GetLiveProgramError(nicolive_program_result)
    else:
      raise GetLiveProgramError(nicolive_program_result)
  else:
    raise GetLiveProgramError(f'Unknown service: {service}')


def guess_service(live_id_or_url: str) -> Optional[Literal['nicolive']]:
  urlp = urlparse(live_id_or_url)

  if urlp.scheme == 'https' and \
     urlp.hostname == 'live.nicovideo.jp':
      return 'nicolive'

  return None
