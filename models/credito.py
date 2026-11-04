from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from models.Geral import Base

class Emprestimo(Base):
    __tablename__ = "solicitacoes_credito"

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor_solicitado = Column(Float, nullable=False)
    taxa_juros = Column(Float, nullable=False, default=0.02)
    valor_total_a_pagar = Column(Float, nullable=False)
    quantidade_parcelas = Column(Integer, nullable=False)
    status = Column(String(30), default="Em Análise")
    data_solicitacao = Column(DateTime, default=datetime.utcnow)

    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)