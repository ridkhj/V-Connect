from flask import Blueprint, jsonify, current_app
from app.scripts.data_extractor import SheetDataExtractor
from app.utils.turn_json import object_to_json
from pathlib import Path

get_cdpr_bp = Blueprint('getcdpr',__name__)

@get_cdpr_bp.route('/get-cdpr', methods=['GET'])
def get_cdpr():
    """
    Obtém dados de CDPR de um arquivo Excel
    ---
    tags:
      - CDPR
    summary: Recupera dados de CDPR processados de um arquivo Excel
    description: Lê um arquivo Excel chamado 'cdpr.xlsx' localizado no diretório 'assets/sheets', processa os dados e retorna um JSON com os dados extraídos. Retorna erros caso o arquivo não exista, esteja vazio ou ocorra um problema durante o processamento.
    produces:
      - application/json
    responses:
      200:
        description: Dados carregados com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  description: Indica se a operação foi bem-sucedida
                  example: true
                data:
                  type: array
                  description: Lista de dados processados do arquivo Excel
                  items:
                    type: object
                    properties:
                      code:
                        type: string
                        description: Código do CDPR
                        example: "CDPR123"
                      name:
                        type: string
                        description: Nome associado ao CDPR
                        example: "João Silva"
                      age:
                        type: integer
                        description: Idade associada ao CDPR
                        example: 30
                message:
                  type: string
                  description: Mensagem de sucesso
                  example: "Dados carregados com sucesso"
      404:
        description: Arquivo não encontrado ou sem dados válidos
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  description: Indica se a operação foi bem-sucedida
                  example: false
                error:
                  type: string
                  description: Mensagem de erro
                  example: "Arquivo não encontrado"
                details:
                  type: string
                  description: Detalhes adicionais sobre o erro
                  example: "Você precisa processar os arquivos primeiro"
                errorType:
                  type: string
                  description: Tipo de erro
                  example: "FILE_NOT_FOUND"
      500:
        description: Erro interno do servidor ou falha na conversão de dados
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  description: Indica se a operação foi bem-sucedida
                  example: false
                error:
                  type: string
                  description: Mensagem de erro
                  example: "Erro interno do servidor"
                details:
                  type: string
                  description: Detalhes adicionais sobre o erro
                  example: "Mensagem de erro específica"
                errorType:
                  type: string
                  description: Tipo de erro
                  example: "SERVER_ERROR"
    """
    try:
        assets_path = Path(__file__).parent.parent.parent / 'assets'
        sheets_path = assets_path / 'sheets'
        file_path = sheets_path / 'cdpr.xlsx'

        if not file_path.exists():
            return jsonify({
                "success": False,
                "error": "Arquivo não encontrado",
                "details": "Você precisa processar os arquivos primeiro",
                "errorType": "FILE_NOT_FOUND"
            }), 404

        sheetExtractor = SheetDataExtractor()
        cdpr = sheetExtractor.unity_process_sheet('cdpr.xlsx')
        
        if not cdpr:
            return jsonify({
                "success": False,
                "error": "Sem dados para processar",
                "details": "O arquivo existe mas está vazio ou não contém dados válidos",
                "errorType": "NO_DATA"
            }), 404

        data = object_to_json(cdpr)
        if isinstance(data, dict) and "error" in data:
            return jsonify({
                "success": False,
                "error": "Erro ao converter dados",
                "details": data["error"],
                "errorType": "CONVERSION_ERROR"
            }), 500

        return jsonify({
            "success": True,
            "data": data,
            "message": "Dados carregados com sucesso"
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro interno: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e),
            "errorType": "SERVER_ERROR"
        }), 500
