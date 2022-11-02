class RoutineMonitor(Processor):
    def __init__(self, conf: Config, log: Log, cnx: Connect, processor: Processor):
        self.conf = conf
        self.log = log
        self.cnx = cnx
        self.n_update_candidates = 0
        self.update_candidates = []

    def update_status(self):
        return update_status.main(self)

    def __image_cleaner(self):
        return clean_images.main(self)

    def __update_calculator_meta(self):
        return update_calc_meta.main(self)

    def regular_checks(self):
        self.__image_cleaner
        self.__update_calculator_meta
        return self
    
    def __archive_wdp_orphans(self):
        return archive_wdp_orphans.main(self)

    def __archive_variation_orphans(self):
        return archive_variation_orphans.main(self)

    def __delete_duplicate_skus(self):
        return delete_duplicate_skus.main(self)

    def __find_products_wo_images(self):
        return find_products_wo_images.main(self)

    def __sync_orders(self):
        return sync_orders.main(self)

    def __add_product_badges(self):
        return add_product_badges.main(self)

    def __dedupe_images(self):
        return dedupe_images.main(self)

    def daily_checks(self):
        self.__archive_wdp_orphans()
        self.__archive_variation_orphans()
        self.__delete_duplicate_skus()
        self.__find_products_wo_images()
        self.__sync_orders()
        self.__add_product_badges()
        self.__dedupe_images()
        return self

    def get_update_candidates(self):
        return get_update_candidates.main(self)

    def __delete_before_update(self):
        return delete_before_update.main(self)

    def preprocessing(self):
        self.__delete_before_update()
        return self

    def finish_flags(
            self, cmd_list=None, cred=False, porcelain=False, **kwargs) -> list:
        return finish_flags.main(self, cmd_list, cred, porcelain, **kwargs)

    def subprocess(self, serv: Literal['wdp', 'tab'], cmd: list) -> Tuple[str, str]:
        return subprocess.main(self, serv, cmd)
