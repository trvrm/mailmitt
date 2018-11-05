import functools
import json
    
dumps=functools.partial(json.dumps,indent=4,ensure_ascii=False,sort_keys=True)



