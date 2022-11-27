from . import liveinfo


"""
  CLI Command
"""


def cli():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('live_id_or_url', type=str)
  parser.add_argument('-s', '--service', type=str, choices=['nicolive'])
  args = parser.parse_args()

  live_id_or_url = args.live_id_or_url
  service = args.service

  print(
    liveinfo.get_live_program(
      live_id_or_url=live_id_or_url,
      service=service,
    )
  )
