from app import login_required, auth_header, db
from app.dependencies.error_response import badRequestError
from flask_restx import Namespace, Resource, fields, reqparse
from flask import request, Response
from app.models.databases import Log
from app.dependencies.type_define import LogType, DeviceTypes, GeneralLogType
from app.dependencies.logger_manager import getAllLogFile, downloadFile
from app.internal.yaml_loader import DOWNLOAD_LOGGER_TOKEN

__NS_URL = 'log'
log_values = [member.value for member in LogType]
module_type = [member.value for member in DeviceTypes]
for member in GeneralLogType:
    module_type.append(member.value)
log = Namespace(__NS_URL.capitalize(), description=f'APIs for {__NS_URL}', path=f'/{__NS_URL}')
log_data = log.model('Log Information', {
    'id': fields.Integer(description='Log id'),
    'type': fields.String(description="Log type: update, error, info"),
    'module': fields.String(description="Module given log"),
    'code': fields.Integer(description="Code of log"),
    'desc': fields.String(description="Desc of log"),
    'date_time': fields.String(description="date time")
})
download = reqparse.RequestParser()
download.add_argument('download_token', location='headers', required=True, 
                         help='Download token header is required')
get_log = reqparse.RequestParser()
get_log.add_argument('type', choices=log_values, help="Filter log by type. Log's type include: update, error, info")
get_log.add_argument('module', choices=module_type, help='Filter log by module')
get_log.add_argument('total',type=int,help='Get latest log')

delete_log = reqparse.RequestParser()
delete_log.add_argument('id', type=int, help="id of log", required=True)

@log.route('/')
class LogAPI(Resource):
    method_decorators = [login_required]
    @log.expect(auth_header, get_log)
    @log.marshal_with(log_data, as_list=True)
    def get(self):
        log_type = request.args.get('type')
        module = request.args.get('module')
        total = request.args.get('total')
        filtered_logs = []
        # Query the devices from the database and filter based on query parameters
        query = db.session.query(Log)
        if (log_type != None) and (module != None) and (total != None):
            if isinstance(log_type, str):
                query = query.filter(Log.log_type == log_type)
            if isinstance(module, str):
                query = query.filter(Log.module == module)
            if not isinstance(module, int):
                query = query.limit(total)
        filtered_logs = query.all()
        return [{
            'id': filtered_log.id, 
            'type': filtered_log.log_type,
            'module': filtered_log.module,
            'code': filtered_log.code,
            'desc': filtered_log.desc,
            'date_time': filtered_log.date_time
        } for filtered_log in filtered_logs]
    
    @log.expect(auth_header, delete_log)
    def delete(self):
        log_id = request.args.get('id')
        error_to_delete = Log.query.filter_by(id=log_id).first()
        return_msg = {}
        if error_to_delete:
            db.session.delete(error_to_delete)
            return_msg['message'] = f"Delete log {id} success"
        else:
            return_msg['message'] = f"No log with id {id}"
        db.session.commit()
        db.session.close()
        return return_msg

@log.route('/download/<int:day>')
class LoggerFileAPI(Resource):
    @log.expect(download)
    def get(self, day: int):
        download_token = request.headers.get('download_token')
        files = getAllLogFile()

        if download_token != DOWNLOAD_LOGGER_TOKEN:
            return badRequestError('Wrong download token')
        elif day not in files:
            return badRequestError('File not available')
        else:
            return downloadFile(files[day])
        
@log.route('/download_csv')
class DownloadCSV(Resource):
    method_decorators = [login_required]
    @log.expect(auth_header)
    def get(self):
        logs = Log.query.all()

        # Create a CSV string
        csv_data = "ID,Module,Code,Log Type,Description,date and time\n"
        for log in logs:
            csv_data += f"{log.id},{log.module},{log.code},{log.log_type},{log.desc},{log.date_time}\n"

        # Create a response with CSV content
        response = Response(csv_data, mimetype='text/csv')
        response.headers["Content-Disposition"] = "attachment; filename=gateway_logs.csv"

        return response