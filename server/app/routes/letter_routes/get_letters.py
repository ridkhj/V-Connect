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
    """
    Obtém dados de cartas processados de uma planilha Excel
    ---
    tags:
      - Cartas
    summary: Recupera dados de cartas de uma planilha Excel específica
    description: Lê uma planilha Excel localizada no diretório 'assets/sheets' com o nome '<type>.xlsx', onde 'type' é um dos valores válidos (reciprocas, nsl ou agradecimento). Processa os dados e retorna um JSON com as cartas extraídas. Retorna erros caso o arquivo não exista, esteja vazio ou ocorra um problema durante o processamento.
    produces:
      - application/json
    parameters:
      - name: type
        in: path
        required: true
        schema:
          type: string
          enum:
            - reciprocas
            - nsl
            - agradecimento
          example: reciprocas
        description: Tipo da planilha a ser processada (sem extensão '.xlsx'). Valores válidos são 'reciprocas', 'nsl' ou 'agradecimento'.
    responses:
      200:
        description: Dados extraídos com sucesso
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
                  description: Lista de cartas extraídas do arquivo Excel
                  items:
                    type: object
                    properties:
                      code:
                        type: string
                        description: Código da carta
                        example: "LTR123"
                      letterCode:
                        type: string
                        description: Código específico da carta
                        example: "LC456"
                      name:
                        type: string
                        description: Nome associado à carta
                        example: "João Silva"
                      type:
                        type: string
                        description: Tipo da carta
                        example: "reciprocas"
                      status:
                        type: string
                        description: Status da carta
                        example: "Enviada"
                      questions:
                        type: array
                        description: Lista de perguntas (presente apenas para cartas do tipo 'reciprocas')
                        items:
                          type: string
                          example: "Qual é o status atual do projeto?"
                message:
                  type: string
                  description: Mensagem de sucesso
                  example: "Dados carregados com sucesso"
      400:
        description: Tipo inválido fornecido
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
                  example: "Erro de validação"
                details:
                  type: string
                  description: Detalhes adicionais sobre o erro
                  example: "Tipo inválido: teste. Tipos válidos: reciprocas, nsl, agradecimento"
                errorType:
                  type: string
                  description: Tipo de erro
                  example: "VALIDATION_ERROR"
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
        description: Erro interno ao processar o arquivo ou servidor
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
                  example: "Erro ao processar arquivo"
                details:
                  type: string
                  description: Detalhes adicionais sobre o erro
                  example: "Erro específico do processamento"
                errorType:
                  type: string
                  description: Tipo de erro
                  example: "PROCESSING_ERROR"
    """
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



