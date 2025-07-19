# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Date, Time, Text, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# --- Tabelas de Junção para Relações Muitos-para-Muitos ---
# professional_service_association: Relaciona Profissionais a Serviços
professional_service_association = Table(
    'professional_service_association', Base.metadata,
    Column('professional_id', Integer, ForeignKey('professionals.id'), primary_key=True),
    Column('service_id', Integer, ForeignKey('services.id'), primary_key=True)
)

# customer_tag_association: Relaciona Clientes a Tags
customer_tag_association = Table(
    'customer_tag_association', Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('system_tags.id'), primary_key=True)
)

# --- Modelos (Tabelas do Banco de Dados) ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="professional") # Ex: "admin", "professional", "receptionist"

    professional = relationship("Professional", back_populates="user", uselist=False)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    birthday = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    appointments = relationship("Appointment", back_populates="customer")
    anamnesis_records = relationship("AnamnesisRecord", back_populates="customer")
    opportunities = relationship("Opportunity", back_populates="customer")
    # Relação muitos-para-muitos com SystemTag através da tabela de associação
    tags = relationship("SystemTag", secondary=customer_tag_association, back_populates="customers")
    conversations = relationship("Conversation", back_populates="customer")


class Professional(Base):
    __tablename__ = "professionals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True) # Opcional: linkar a um usuário de login
    name = Column(String(255), nullable=False)
    color = Column(String(50)) # Ex: "bg-pink-400" para a UI do front-end

    user = relationship("User", back_populates="professional")
    appointments = relationship("Appointment", back_populates="professional")
    # Relação muitos-para-muitos com Service através da tabela de associação
    services = relationship("Service", secondary=professional_service_association, back_populates="professionals")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    duration = Column(Integer, nullable=False) # Duração em minutos
    price = Column(Float, nullable=False)
    description = Column(Text)

    appointments = relationship("Appointment", back_populates="service")
    professionals = relationship("Professional", secondary=professional_service_association, back_populates="services")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False) # Formato HH:MM:SS
    status = Column(String(50), default="Confirmado") # Ex: "Confirmado", "Pendente", "Cancelado", "Concluído"
    notes = Column(Text) # Observações específicas do agendamento
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    professional = relationship("Professional", back_populates="appointments")
    anamnesis_record = relationship("AnamnesisRecord", back_populates="appointment", uselist=False)


class AnamnesisTemplateField(Base):
    __tablename__ = "anamnesis_template_fields"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False) # Chave para o campo (ex: 'queixa_principal')
    label = Column(String(255), nullable=False) # Rótulo para exibição (ex: 'Queixa Principal')
    field_type = Column(String(50), nullable=False) # Ex: 'text', 'textarea', 'radio', 'select'
    options = Column(JSON) # Para radio/select, armazena as opções como JSON (ex: ["Sim", "Não"])
    order = Column(Integer, default=0) # Ordem de exibição do campo

class AnamnesisRecord(Base):
    __tablename__ = "anamnesis_records"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False) # FK para o agendamento
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    record_date = Column(Date, default=func.now()) # Data da criação da ficha
    data = Column(JSON, nullable=False) # Armazena as respostas da anamnese como um JSON

    appointment = relationship("Appointment", back_populates="anamnesis_record")
    customer = relationship("Customer", back_populates="anamnesis_records")

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    value = Column(Float, nullable=False)
    stage = Column(String(50), default="Lead") # Ex: "Lead", "Follow Up", "Proposta", "Negociação", "Fechado", "Perdido"
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="opportunities")

class SystemTag(Base):
    __tablename__ = "system_tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(50)) # Ex: "bg-yellow-400" para a UI do front-end

    customers = relationship("Customer", secondary=customer_tag_association, back_populates="tags")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True, nullable=False)
    last_message_at = Column(DateTime, default=func.now(), onupdate=func.now())
    unread_count = Column(Integer, default=0) # Contagem de mensagens não lidas pela clínica

    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(50), nullable=False) # Ex: "clinic", "customer"
    message_type = Column(String(50), default="text") # Ex: "text", "image", "audio", "file"
    content = Column(JSON, nullable=False) # Conteúdo da mensagem (texto, URL da imagem, etc.)
    timestamp = Column(DateTime, default=func.now())

    conversation = relationship("Conversation", back_populates="messages")

class ClinicInfo(Base):
    __tablename__ = "clinic_info"
    id = Column(Integer, primary_key=True, index=True) # Geralmente terá apenas uma linha (id=1)
    name = Column(String(255), nullable=False)
    phone = Column(String(50))
    address = Column(String(255))
    working_hours = Column(String(255))
