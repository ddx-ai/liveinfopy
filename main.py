import live_info_api_client

application_useragent = 'live_info_api_client_py/0.1.0+dev (+https://github.com/aoirint/live_info_api_client_py)'
useragent = f'facebookexternalhit/1.1;Googlebot/2.1;{application_useragent}'


def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('live_id_or_url', type=str)
  args = parser.parse_args()

  live_id_or_url = args.live_id_or_url

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

if __name__ == '__main__':
  main()
