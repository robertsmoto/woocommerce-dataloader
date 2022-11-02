from . import strip_bad_characters
from flag.methods import finish_flags
from typing import Tuple

def main(self, wdp_path: str, info_by_wdppath: dict, featured_image: dict) -> Tuple[str, str]:
    """Uploads images from staging to wdp media library."""

    image = info_by_wdppath[wdp_path].get('image', {})

    cmd_lst = ['wp', 'media', 'import', wdp_path]

    # check featured and determine if the featured_image flag should be added
    if featured_image.get('path', '') == wdp_path:
        cmd_lst.append('--featured_image')

    cmd_lst = finish_flags.main(
            self,
            cmd_lst=cmd_lst,
            title=image.get('title', ''),
            caption=image.get('caption', ''),
            alt=strip_bad_characters.main(image.get('alt', 'no text provided')),
            desc=image.get('description', ''),
            cred=True,
            porcelain=True
            )

    wdp_id, err = self.cnx.subprocess('wdp', cmd_lst)

    # only warning, not failing based on this err, for now
    if err:
        self.log.warn(f"imagesupload_images {err}")
        return 'placeholder image', '339729'

    return wdp_id, ''
