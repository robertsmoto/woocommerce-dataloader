from . methods import *
from abc import ABC
from data.data import CheckerData


class Checker(ABC):

    def __init__(self, data: CheckerData):
        self.d = data

    def check(self):
        ...

class NormalChecker(Checker):

    def check(self):
        update_status.main(self)
        # archive_variation_orphans
        # archive_wdp_orphans
        # clean_images
        # dedup_images
        # delete_duplicate_skus
        # find_products_wo_images

class DailyChecker(Checker):

    def check(self):
        ...

class SpecialChecker(Checker):

    def check(self):
        ...
