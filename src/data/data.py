from connection.connection import Connect
from config.config import Config
from log.log import Log
from dataclasses import dataclass, field


@dataclass
class ProcessorData:
    """Class contains config, connection, logger and data store."""
    err: str = ''

    product_data: list = field(default_factory=list)
    cleaned_data: list = field(default_factory=list)
    cli_pid_group: int = 0
    # 'wdp_id' and 'crud_operation' additionally set on each record

    komplexity: str = 'simple'
    vapr_sku: str = ''
    vapr_id: int = 0
    vapr_operation: str = 'update'
    vapr_quantity: int = 0
    vapr_in_stock: bool = True
    vapr_manage_stock: bool = False

    # master list for main products, both variable and simple
    attributes_list: list = field(default_factory=list)
    # index by sku for variations
    attributes_index: dict = field(default_factory=dict) 

    # for images
    image_data: list = field(default_factory=list)
    info_by_wdppath: dict = field(default_factory=dict)
    wdppaths_by_sku: dict = field(default_factory=dict)
    featured_image: dict = field(default_factory=dict)

    # finished subprocess commands for the cli
    vapr_cmd_lst: list = field(default_factory=list)
    variation_cmd_lst: list = field(default_factory=list)
    simple_cmd_lst: list = field(default_factory=list)
    brand: str = ''
    wdp_ids: list = field(default_factory=list) #<-- used for brands


@dataclass
class CheckerData:
    """Class contains config, connection, logger and data store."""
    conf: Config
    cnx: Connect
    log: Log
    err: str = ''
