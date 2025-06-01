from tkinter.messagebox import RETRY
from flask import Blueprint, jsonify
from flask import request
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json
import os
from flask import current_app
from pathlib import Path


get_letters_bp = Blueprint('getletters',__name__, url_prefix='/get-letters')

def get_letters(type):
    try:
        type = validate_type(type)
        
        assets_path = Path(__file__).parent.parent.parent / 'assets'
        sheets_path = assets_path / 'sheets'
        file_path = sheets_path / type

        if not file_path.exists():
            return jsonify({
                "success": False,
                "error": "Arquivo não encontrado",
                "details": f"Você precisa processar os arquivos primeiro",
                "errorType": "FILE_NOT_FOUND"
            }), 404

        try:
            sheetExtractor = SheetDataExtractor()
            letters = sheetExtractor.unity_process_sheet(type)
            
            if not letters:
                return jsonify({
                    "success": False,
                    "error": "Sem dados para processar",
                    "details": "O arquivo existe mas está vazio ou não contém dados válidos",
                    "errorType": "NO_DATA"
                }), 404


            letters_json = object_to_json(letters)
            return jsonify({
                "success": True,
                "data": letters_json,
                "message": "Dados carregados com sucesso"
            }), 200

        except Exception as e:
            current_app.logger.error(f"Erro ao processar arquivo {type}: {str(e)}")
            return jsonify({
                "success": False,
                "error": "Erro ao processar arquivo",
                "details": str(e),
                "errorType": "PROCESSING_ERROR"
            }), 500

    except ValueError as e:
        return jsonify({
            "success": False,
            "error": "Erro de validação",
            "details": str(e),
            "errorType": "VALIDATION_ERROR"
        }), 400
    except Exception as e:
        current_app.logger.error(f"Erro interno: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e),
            "errorType": "SERVER_ERROR"
        }), 500

get_letters_bp.get('/<type>')(get_letters)

def validate_type(type):
    valid_types = ['reciprocas', 'nsl', 'agradecimento']
    if type not in valid_types:
        raise ValueError(f"Tipo inválido: {type}. Tipos válidos: {', '.join(valid_types)}")
    return type + '.xlsx'



