from subconscious.model import RedisModel, Column

class Host(RedisModel):
    ip_address   = Column(type=str, primary_key=True)
    scanned_at   = Column(type=str, required=True)
    scan_results = Column(type=str, required=True)
    up           = Column(type=int, required=True, index=True)
