import json

from ttdclient.models.base import Base


class Creative(Base):

    obj_name = "creative"
    
    def get_size(self):
        
        attributes = [
            'ImageAttributes',
            'FacebookAttributes',
            'FacebookPagePostAttributes',
            'FlashAttributes',
            'ThirdPartyTagAttributes',
            'TradeDeskHostedVideoAttributes',
            'ThirdPartyHostedVideoAttributes',
            ]

        width = 0
        height = 0
        for attribute in attributes:
            fields = self.get(attribute, None)
            if not fields:
                continue

            width = fields.get('Width')
            height = fields.get('Height')
            
        return [width, height]
