from typing import Optional, List, Literal, Union
import requests
from dataclasses import dataclass


"""
  Public APIs
"""


@dataclass
class GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail:
  url: str
  width: int
  height: int


@dataclass
class GetYtliveProgramsSuccessYtliveProgramDataItemThumbnails:
  default: Optional[GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail]
  medium: Optional[GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail]
  high: Optional[GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail]
  standard: Optional[GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail]
  maxres: Optional[GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail]


@dataclass
class GetYtliveProgramsSuccessYtliveProgramDataItemStatus:
  upload_status: Union[Literal['processed', 'uploaded'], str]
  privacy_status: Union[Literal['public'], str]


@dataclass
class GetYtliveProgramsSuccessYtliveProgramDataItemLiveStreamingDetails:
  actual_start_time: Optional[str]
  actual_end_time: Optional[str]
  scheduled_start_time: Optional[str]
  scheduled_end_time: Optional[str]
  concurrent_viewers: Optional[str]


@dataclass
class GetYtliveProgramsSuccessYtliveProgramDataItem:
  channel_id: str
  channel_title: str
  video_id: str
  title: str
  description: str
  live_broadcast_content: str
  status: GetYtliveProgramsSuccessYtliveProgramDataItemStatus
  thumbnails: GetYtliveProgramsSuccessYtliveProgramDataItemThumbnails
  live_streaming_details: \
    GetYtliveProgramsSuccessYtliveProgramDataItemLiveStreamingDetails


@dataclass
class GetYtliveProgramsSuccessYtliveProgramData:
  items: List[GetYtliveProgramsSuccessYtliveProgramDataItem]


@dataclass
class GetYtliveProgramsSuccessYtliveProgramResult:
  result_type: Literal['success']
  data_type: Literal['ytlive_programs']
  data: GetYtliveProgramsSuccessYtliveProgramData


@dataclass
class GetYtliveProgramsBadRequestResult:
  result_type: Literal['bad_request']


@dataclass
class GetYtliveProgramsForbiddenResult:
  result_type: Literal['forbidden']


@dataclass
class GetYtliveProgramsMaintenanceResult:
  result_type: Literal['maintenance']


@dataclass
class GetYtliveProgramsUnknownErrorResult:
  result_type: Literal['unknown_error']


GetYtliveProgramsResult = Union[
  GetYtliveProgramsSuccessYtliveProgramResult,
  GetYtliveProgramsBadRequestResult,
  GetYtliveProgramsForbiddenResult,
  GetYtliveProgramsMaintenanceResult,
  GetYtliveProgramsUnknownErrorResult,
]


def get_ytlive_programs(
  channel_id: str,
  useragent: str,
  api_key: str,
  max_results: Optional[int] = None,
) -> GetYtliveProgramsResult:
  search_list_video_result = get_ytlive_search_list_video(
    channel_id=channel_id,
    useragent=useragent,
    api_key=api_key,
    max_results=max_results,
  )
  if search_list_video_result.result_type == 'success':
    if search_list_video_result.data_type == 'ytlive_programs':
      search_list_video_items = search_list_video_result.data.items

      video_ids = [
        search_list_video_item.video_id
        for search_list_video_item in search_list_video_items
      ]

      videos_list_result = get_ytlive_videos_list(
        id=','.join(video_ids),
        useragent=useragent,
        api_key=api_key,
      )

      if videos_list_result.result_type == 'success':
        if videos_list_result.data_type == 'ytlive_programs':
          videos_list_items = videos_list_result.data.items

          items: List[GetYtliveProgramsSuccessYtliveProgramDataItem] = []
          for videos_list_item in videos_list_items:
            if videos_list_item.status.privacy_status != 'public':
              continue  # drop not-public (private and unlisted) videos

            live_streaming_details = (
              GetYtliveProgramsSuccessYtliveProgramDataItemLiveStreamingDetails(  # noqa: E501
                actual_start_time=(
                  videos_list_item.live_streaming_details.actual_start_time
                ),
                actual_end_time=(
                  videos_list_item.live_streaming_details.actual_end_time
                ),
                scheduled_start_time=(
                  videos_list_item.live_streaming_details.scheduled_start_time
                ),
                scheduled_end_time=(
                  videos_list_item.live_streaming_details.scheduled_end_time
                ),
                concurrent_viewers=(
                  videos_list_item.live_streaming_details.concurrent_viewers
                ),
              )
            )

            items.append(
              GetYtliveProgramsSuccessYtliveProgramDataItem(
                channel_id=videos_list_item.channel_id,
                channel_title=videos_list_item.channel_title,
                video_id=videos_list_item.video_id,
                title=videos_list_item.title,
                description=videos_list_item.description,
                live_broadcast_content=videos_list_item.live_broadcast_content,
                status=GetYtliveProgramsSuccessYtliveProgramDataItemStatus(
                  upload_status=videos_list_item.status.upload_status,
                  privacy_status=videos_list_item.status.privacy_status,
                ),
                thumbnails=(
                  GetYtliveProgramsSuccessYtliveProgramDataItemThumbnails(
                    default=(
                      GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail(
                        url=videos_list_item.thumbnails.default.url,
                        width=videos_list_item.thumbnails.default.width,
                        height=videos_list_item.thumbnails.default.height,
                      )
                      if videos_list_item.thumbnails.default is not None
                      else None
                    ),
                    medium=(
                      GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail(
                        url=videos_list_item.thumbnails.medium.url,
                        width=videos_list_item.thumbnails.medium.width,
                        height=videos_list_item.thumbnails.medium.height,
                      )
                      if videos_list_item.thumbnails.medium is not None
                      else None
                    ),
                    high=(
                      GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail(
                        url=videos_list_item.thumbnails.high.url,
                        width=videos_list_item.thumbnails.high.width,
                        height=videos_list_item.thumbnails.high.height,
                      )
                      if videos_list_item.thumbnails.high is not None
                      else None
                    ),
                    standard=(
                      GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail(
                        url=videos_list_item.thumbnails.standard.url,
                        width=videos_list_item.thumbnails.standard.width,
                        height=videos_list_item.thumbnails.standard.height,
                      )
                      if videos_list_item.thumbnails.standard is not None
                      else None
                    ),
                    maxres=(
                      GetYtliveProgramsSuccessYtliveProgramDataItemThumbnail(
                        url=videos_list_item.thumbnails.maxres.url,
                        width=videos_list_item.thumbnails.maxres.width,
                        height=videos_list_item.thumbnails.maxres.height,
                      )
                      if videos_list_item.thumbnails.maxres is not None
                      else None
                    ),
                  )
                ),
                live_streaming_details=live_streaming_details,
              )
            )

          return GetYtliveProgramsSuccessYtliveProgramResult(
            result_type='success',
            data_type='ytlive_programs',
            data=GetYtliveProgramsSuccessYtliveProgramData(
              items=items,
            ),
          )

      elif videos_list_result.result_type == 'bad_request':
        return GetYtliveProgramsBadRequestResult(
          result_type='bad_request',
        )

      elif videos_list_result.result_type == 'forbidden':
        return GetYtliveProgramsForbiddenResult(
          result_type='forbidden',
        )

      elif videos_list_result.result_type == 'maintenance':
        return GetYtliveProgramsMaintenanceResult(
          result_type='maintenance',
        )

  return GetYtliveProgramsUnknownErrorResult(
    result_type='unknown_error',
  )


"""
  Private API: Search: list
"""


@dataclass
class GetYtliveSearchListSuccessYtliveProgramDataItemThumbnail:
  url: str
  width: int
  height: int


@dataclass
class GetYtliveSearchListSuccessYtliveProgramDataItemThumbnails:
  default: Optional[GetYtliveSearchListSuccessYtliveProgramDataItemThumbnail]
  medium: Optional[GetYtliveSearchListSuccessYtliveProgramDataItemThumbnail]
  high: Optional[GetYtliveSearchListSuccessYtliveProgramDataItemThumbnail]


@dataclass
class GetYtliveSearchListSuccessYtliveProgramDataItem:
  channel_id: str
  channel_title: str
  video_id: str
  title: str
  description: str
  live_broadcast_content: str
  thumbnails: GetYtliveSearchListSuccessYtliveProgramDataItemThumbnails


@dataclass
class GetYtliveSearchListSuccessYtliveProgramData:
  items: List[GetYtliveSearchListSuccessYtliveProgramDataItem]


@dataclass
class GetYtliveSearchListSuccessYtliveProgramResult:
  result_type: Literal['success']
  data_type: Literal['ytlive_programs']
  data: GetYtliveSearchListSuccessYtliveProgramData


@dataclass
class GetYtliveSearchListBadRequestResult:
  result_type: Literal['bad_request']


@dataclass
class GetYtliveSearchListForbiddenResult:
  result_type: Literal['forbidden']


@dataclass
class GetYtliveSearchListMaintenanceResult:
  result_type: Literal['maintenance']


@dataclass
class GetYtliveSearchListUnknownErrorResult:
  result_type: Literal['unknown_error']


GetYtliveSearchListResult = Union[
  GetYtliveSearchListSuccessYtliveProgramResult,
  GetYtliveSearchListBadRequestResult,
  GetYtliveSearchListForbiddenResult,
  GetYtliveSearchListMaintenanceResult,
  GetYtliveSearchListUnknownErrorResult,
]


def get_ytlive_search_list_video(
  channel_id: str,
  useragent: str,
  api_key: str,
  max_results: Optional[int] = None,
) -> GetYtliveSearchListResult:
  search_api_url = 'https://www.googleapis.com/youtube/v3/search'
  params = {
    'key': api_key,
    'part': 'id,snippet',
    'channelId': channel_id,
    'type': 'video',
    'order': 'date',  # createdAt desc
  }
  if max_results is not None:
    params['maxResults'] = str(max_results)

  headers = {
    'User-Agent': useragent,
  }

  search_res = requests.get(search_api_url, headers=headers, params=params)
  search_status = search_res.status_code

  if search_status == 200:
    search_response = search_res.json()
    search_response_items = search_response.get('items', [])

    items: List[GetYtliveSearchListSuccessYtliveProgramDataItem] = []
    for response_item in search_response_items:
      id = response_item['id']
      video_id = id['videoId']

      snippet = response_item['snippet']
      snippet_channel_id = snippet['channelId']
      snippet_channel_title = snippet['channelTitle']

      thumbnails = snippet['thumbnails']
      thumbnail_default = thumbnails.get('default')
      thumbnail_medium = thumbnails.get('medium')
      thumbnail_high = thumbnails.get('high')

      items.append(GetYtliveSearchListSuccessYtliveProgramDataItem(
        channel_id=snippet_channel_id,
        channel_title=snippet_channel_title,
        video_id=video_id,
        title=snippet['title'],
        description=snippet['description'],
        live_broadcast_content=snippet['liveBroadcastContent'],
        thumbnails=GetYtliveSearchListSuccessYtliveProgramDataItemThumbnails(
          default=GetYtliveSearchListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_default['url'],
            width=thumbnail_default['width'],
            height=thumbnail_default['height'],
          ) if thumbnail_default is not None else None,
          medium=GetYtliveSearchListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_medium['url'],
            width=thumbnail_medium['width'],
            height=thumbnail_medium['height'],
          ) if thumbnail_medium is not None else None,
          high=GetYtliveSearchListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_high['url'],
            width=thumbnail_high['width'],
            height=thumbnail_high['height'],
          ) if thumbnail_high is not None else None,
        ),
      ))

    return GetYtliveSearchListSuccessYtliveProgramResult(
      result_type='success',
      data_type='ytlive_programs',
      data=GetYtliveSearchListSuccessYtliveProgramData(
        items=items,
      )
    )

  elif search_status == 400:
    return GetYtliveSearchListBadRequestResult(
      result_type='bad_request',
    )

  elif search_status == 403:
    return GetYtliveSearchListForbiddenResult(
      result_type='forbidden',
    )

  elif search_status == 500:
    return GetYtliveSearchListMaintenanceResult(
      result_type='maintenance',
    )

  return GetYtliveSearchListUnknownErrorResult(
    result_type='unknown_error',
  )


"""
  Private API: Videos: list
"""


@dataclass
class GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail:
  url: str
  width: int
  height: int


@dataclass
class GetYtliveVideosListSuccessYtliveProgramDataItemThumbnails:
  default: Optional[GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail]
  medium: Optional[GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail]
  high: Optional[GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail]
  standard: Optional[GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail]
  maxres: Optional[GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail]


@dataclass
class GetYtliveVideosListSuccessYtliveProgramDataItemStatus:
  upload_status: Union[Literal['processed', 'uploaded'], str]
  privacy_status: Union[Literal['private', 'public', 'unlisted'], str]


@dataclass
class GetYtliveVideosListSuccessYtliveProgramDataItemLiveStreamingDetails:
  actual_start_time: Optional[str]
  actual_end_time: Optional[str]
  scheduled_start_time: Optional[str]
  scheduled_end_time: Optional[str]
  concurrent_viewers: Optional[str]


@dataclass
class GetYtliveVideosListSuccessYtliveProgramDataItem:
  channel_id: str
  channel_title: str
  video_id: str
  title: str
  description: str
  live_broadcast_content: str
  status: GetYtliveVideosListSuccessYtliveProgramDataItemStatus
  thumbnails: GetYtliveVideosListSuccessYtliveProgramDataItemThumbnails
  live_streaming_details: \
    GetYtliveVideosListSuccessYtliveProgramDataItemLiveStreamingDetails


@dataclass
class GetYtliveVideosListSuccessYtliveProgramData:
  items: List[GetYtliveVideosListSuccessYtliveProgramDataItem]


@dataclass
class GetYtliveVideosListSuccessYtliveProgramResult:
  result_type: Literal['success']
  data_type: Literal['ytlive_programs']
  data: GetYtliveVideosListSuccessYtliveProgramData


@dataclass
class GetYtliveVideosListBadRequestResult:
  result_type: Literal['bad_request']


@dataclass
class GetYtliveVideosListForbiddenResult:
  result_type: Literal['forbidden']


@dataclass
class GetYtliveVideosListMaintenanceResult:
  result_type: Literal['maintenance']


@dataclass
class GetYtliveVideosListUnknownErrorResult:
  result_type: Literal['unknown_error']


GetYtliveVideosListResult = Union[
  GetYtliveVideosListSuccessYtliveProgramResult,
  GetYtliveVideosListBadRequestResult,
  GetYtliveVideosListForbiddenResult,
  GetYtliveVideosListMaintenanceResult,
  GetYtliveVideosListUnknownErrorResult,
]


def get_ytlive_videos_list(
  id: str,  # video id (comma-separated)
  useragent: str,
  api_key: str,
) -> GetYtliveVideosListResult:
  videos_api_url = 'https://www.googleapis.com/youtube/v3/videos'
  params = {
    'key': api_key,
    'part': 'snippet,status,liveStreamingDetails',
    'id': id,
  }

  headers = {
    'User-Agent': useragent,
  }

  videos_res = requests.get(videos_api_url, headers=headers, params=params)
  videos_status = videos_res.status_code

  if videos_status == 200:
    videos_response = videos_res.json()
    videos_response_items = videos_response.get('items', [])

    items: List[GetYtliveVideosListSuccessYtliveProgramDataItem] = []
    for response_item in videos_response_items:
      video_id = response_item['id']

      snippet = response_item['snippet']
      snippet_channel_id = snippet['channelId']
      snippet_channel_title = snippet['channelTitle']

      thumbnails = snippet['thumbnails']
      thumbnail_default = thumbnails.get('default')
      thumbnail_medium = thumbnails.get('medium')
      thumbnail_high = thumbnails.get('high')
      thumbnail_standard = thumbnails.get('standard')
      thumbnail_maxres = thumbnails.get('maxres')

      status = response_item['status']
      upload_status: str = status['uploadStatus']
      privacy_status: str = status['privacyStatus']

      live_streaming_details = response_item.get('liveStreamingDetails')
      if live_streaming_details is None:
        continue  # this is a normal video. not live or archive

      actual_start_time = live_streaming_details.get('actualStartTime')
      actual_end_time = live_streaming_details.get('actualEndTime')
      scheduled_start_time = live_streaming_details.get('scheduledStartTime')
      scheduled_end_time = live_streaming_details.get('scheduledEndTime')
      concurrent_viewers = live_streaming_details.get('concurrentViewers')

      items.append(GetYtliveVideosListSuccessYtliveProgramDataItem(
        channel_id=snippet_channel_id,
        channel_title=snippet_channel_title,
        video_id=video_id,
        title=snippet['title'],
        description=snippet['description'],
        live_broadcast_content=snippet['liveBroadcastContent'],
        thumbnails=GetYtliveVideosListSuccessYtliveProgramDataItemThumbnails(
          default=GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_default['url'],
            width=thumbnail_default['width'],
            height=thumbnail_default['height'],
          ) if thumbnail_default is not None else None,
          medium=GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_medium['url'],
            width=thumbnail_medium['width'],
            height=thumbnail_medium['height'],
          ) if thumbnail_medium is not None else None,
          high=GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_high['url'],
            width=thumbnail_high['width'],
            height=thumbnail_high['height'],
          ) if thumbnail_high is not None else None,
          standard=GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_standard['url'],
            width=thumbnail_standard['width'],
            height=thumbnail_standard['height'],
          ) if thumbnail_standard is not None else None,
          maxres=GetYtliveVideosListSuccessYtliveProgramDataItemThumbnail(
            url=thumbnail_maxres['url'],
            width=thumbnail_maxres['width'],
            height=thumbnail_maxres['height'],
          ) if thumbnail_maxres is not None else None,
        ),
        status=GetYtliveVideosListSuccessYtliveProgramDataItemStatus(
          upload_status=upload_status,
          privacy_status=privacy_status,
        ),
        live_streaming_details=(
          GetYtliveVideosListSuccessYtliveProgramDataItemLiveStreamingDetails(
            actual_start_time=actual_start_time,
            actual_end_time=actual_end_time,
            scheduled_start_time=scheduled_start_time,
            scheduled_end_time=scheduled_end_time,
            concurrent_viewers=concurrent_viewers,
          )
        ),
      ))

    return GetYtliveVideosListSuccessYtliveProgramResult(
      result_type='success',
      data_type='ytlive_programs',
      data=GetYtliveVideosListSuccessYtliveProgramData(
        items=items,
      )
    )

  elif videos_status == 400:
    return GetYtliveVideosListBadRequestResult(
      result_type='bad_request',
    )

  elif videos_status == 403:
    return GetYtliveVideosListForbiddenResult(
      result_type='forbidden',
    )

  elif videos_status == 500:
    return GetYtliveVideosListMaintenanceResult(
      result_type='maintenance',
    )

  return GetYtliveVideosListUnknownErrorResult(
    result_type='unknown_error',
  )
