from .methods import *
from processor.processor import Processor
from data.data import ProcessorData


class Image(Processor):

    def process(self, data: ProcessorData) -> ProcessorData:

        def load_to_temp(self):
            self.log.debug("loading images to temp ...")

            infobypath = data.info_by_wdppath
            for wdp_path, _ in infobypath.items():
                upload_image_staging.main(self, wdp_path, infobypath)
            return self

        def load_to_wdp(self):
            self.log.debug("loading images to wdp ...")

            infobypath = data.info_by_wdppath
            fi = data.featured_image
            for wdp_path, _ in infobypath.items():
                # upoload images
                wdp_id, err = upload_image_to_wdp.main(self, wdp_path, infobypath, fi)
                data.info_by_wdppath[wdp_path]['wdp_id'] = wdp_id
                data.err = err if err else ''
                # send reporting
                if not data.err:
                    self.log.info(f"Success: created image {wdp_id} {wdp_path}")

            return self

        # select the images
        pid = data.cli_pid_group
        image_data, err = select_tab_images_by_pid.main(self, str(pid))
        data.image_data = image_data

        if len(image_data) < 1:
            self.log.warn("No images returned from select.")

        # get first sku
        first_product = data.cleaned_data[0] if data.cleaned_data else {}
        sku = first_product.get('sku', '')
        pathsbysku, infobypath, fi = create_image_index.main(self, image_data, sku)
        data.wdppaths_by_sku = pathsbysku
        data.info_by_wdppath = infobypath
        data.featured_image = fi

        # validate data / check that the client files exist
        for wdp_path, _ in data.info_by_wdppath.items():
            cli_path = data.info_by_wdppath[wdp_path].get('cli_path', '')
            exists, err = check_file_exists.main(self, 'cli', cli_path)
            if not exists:
                self.log.warn(f"Image does not exists: {cli_path} {err}")
                break

        # now load
        load_to_temp(self)
        load_to_wdp(self) 
        # now all needed images are indexed and loaded

        delete_images_staging.main(self, data.info_by_wdppath)

        return data
