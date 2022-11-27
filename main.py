from urllib.parse import urlparse
from typing import Optional, Literal
import live_info_api_client

application_useragent = 'live_info_api_client_py/0.1.0+dev (+https://github.com/aoirint/live_info_api_client_py)'
useragent = f'facebookexternalhit/1.1;Googlebot/2.1;{application_useragent}'


def guess_service(live_id_or_url: str) -> Optional[Literal['nicolive']]:
  urlp = urlparse(live_id_or_url)

  if urlp.scheme == 'https' and \
     urlp.hostname == 'live.nicovideo.jp':
      return 'nicolive'

  return None


def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--service', type=str, choices=['nicolive'])
  parser.add_argument('live_id_or_url', type=str)
  args = parser.parse_args()

  service = args.service
  live_id_or_url = args.live_id_or_url

  if service is None:
    service = guess_service(live_id_or_url=live_id_or_url)

  if service is None:
    raise Exception('Service not specified and auto selection failed. Specify an argument: --service=[nicolive]')

  if service == 'nicolive':
    nicolive_program_result = live_info_api_client.nicolive.get_nicolive_program(
      live_id_or_url=live_id_or_url,
      useragent=useragent,
    )
    if nicolive_program_result.result_type == 'success':
      if nicolive_program_result.data_type == 'nicolive_program':
        print(nicolive_program_result.data)
      else:
        raise Exception(nicolive_program_result)
    else:
      raise Exception(nicolive_program_result)
  else:
    raise Exception(f'Unknown service: {service}')

if __name__ == '__main__':
  main()
