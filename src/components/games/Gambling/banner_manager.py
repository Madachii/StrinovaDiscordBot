from components.games.gambling.strinovabanner import Banner

class BannerManager:
    _banners = set()
    
    @classmethod
    def load_banner(cls, db, logger, uuid: str, banner_name: str):
        banner = Banner(uuid=uuid, db=db, title=banner_name, logger=logger)
        cls._banners.add(banner)
        
    @classmethod
    def remove_banner_by_uuid(cls, uuid):
        for banner in cls._banners:
            if (banner.uuid == uuid):
                cls._banners.remove(banner)
    @classmethod
    def get_banner_from_uuid(cls, uuid):
        for banner in cls._banners:
            if (banner.uuid == uuid):
                return banner
        return None
    
    @classmethod
    def get_full_banner(cls):
        return cls._banners
    
    @classmethod
    def is_empty(cls):
        return len(cls._banners) <= 0