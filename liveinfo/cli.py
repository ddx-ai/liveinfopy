import os
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass,asdict

from . import liveinfo


"""
  CLI Command
"""


def cli():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('live_id_or_url', type=str)
  parser.add_argument(
    '-s', '--service', type=str,
    choices=['nicolive', 'ytlive'],
  )
  parser.add_argument(
    '--ytlive_api_key', type=str,
    default=os.environ.get('LIVEINFO_YTLIVE_API_KEY'),
  )
  parser.add_argument(
    '--ytlive_api_key_file', type=str,
    default=os.environ.get('LIVEINFO_YTLIVE_API_KEY_FILE'),
  )
  parser.add_argument(
    '--output', type=str,
    default='output.txt',
  )
  args = parser.parse_args()

  live_id_or_url: str = args.live_id_or_url
  service: Optional[str] = args.service
  output_path: str = args.output
  ytlive_api_key: Optional[str] = args.ytlive_api_key
  ytlive_api_key_file: Optional[str] = args.ytlive_api_key_file
  if ytlive_api_key_file:
    ytlive_api_key = (
      Path(ytlive_api_key_file).read_text(encoding='utf-8').strip()
    )

  result=liveinfo.get_live_program(
    live_id_or_url=live_id_or_url,
    service=service,
    ytlive_api_key=ytlive_api_key,
  )
  
  with open(output_path, "w",encoding="utf-8") as output_file:
    json.dump(asdict(result),output_file,ensure_ascii=False, indent=4)
