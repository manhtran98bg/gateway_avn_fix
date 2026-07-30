from app.models.databases import Log
from app import db
from typing import Union

def createLog(module: Union[str, any], code: Union[int, any], 
              log_type: Union[str, any], desc: str, commit: bool = True):
    module = module if isinstance(module, str) else module.value
    code = code if isinstance(code, int) else code.value
    log_type = log_type if isinstance(log_type, str) else log_type.value
    new_log = Log(
        module=module,
        code=code,
        log_type=log_type,
        desc=desc
    )
    db.session.add(new_log)
    if commit:
        db.session.commit()
        db.session.close()