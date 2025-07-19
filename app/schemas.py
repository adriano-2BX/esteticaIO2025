# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import date, time, datetime

# --- Schemas Básicos e Utilitários ---
class MessageResponse(BaseModel):
    """Schema para mensagens de resposta genéricas da API."""
    message: str

class Token(BaseModel):
    """Schema para o token de autenticação."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema para os dados decodificados do token (sub, roles)."""
    email: Optional[str] = None
    # Podemos adicionar 'roles: List[str]' se tivermos mais granularidade de permissões

# --- Schemas para Modelos do Banco de Dados ---

# User
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str = "professional" # Default role for new users

class UserCreate(UserBase):
    password: str = Field(..., min_length=6) # Senha é necessária na criação, mas não retornada

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True # Permite que o Pydantic mapeie campos de objetos ORM

# Customer
class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    notes: Optional[str] = None

class CustomerCreate(CustomerBase):
    # Pode adicionar validações específicas para criação se necessário
    pass

class CustomerUpdate(CustomerBase):
    # Todos os campos são opcionais para update (PATCH)
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    notes: Optional[str] = None

class CustomerTag(BaseModel):
    id: int
    name: str
    color: str
    class Config:
        from_attributes = True

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[CustomerTag] = [] # Inclui as tags associadas
    class Config:
        from_attributes = True

# Professional
class ProfessionalBase(BaseModel):
    name: str = Field(..., min_length=2)
    color: Optional[str] = "bg-gray-400" # Cor padrão, se não for fornecida

class ProfessionalCreate(ProfessionalBase):
    user_id: Optional[int] = None # Pode ser vinculado a um usuário existente
    service_ids: List[int] = [] # IDs dos serviços que o profissional oferece

class ProfessionalUpdate(ProfessionalBase):
    name: Optional[str] = None
    color: Optional[str] = None
    user_id: Optional[int] = None
    service_ids: Optional[List[int]] = None

class ProfessionalResponse(ProfessionalBase):
    id: int
    user: Optional[UserResponse] = None # Pode incluir dados do usuário associado
    # services: List[ServiceResponse] = [] # Pode ser adicionado mais tarde para evitar recursão
    class Config:
        from_attributes = True

# Service
class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2)
    duration: int = Field(..., gt=0) # Duração em minutos, deve ser maior que 0
    price: float = Field(..., ge=0) # Preço, deve ser maior ou igual a 0
    description: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    name: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None

class ServiceResponse(ServiceBase):
    id: int
    class Config:
        from_attributes = True

# Appointment
class AppointmentBase(BaseModel):
    customer_id: int
    service_id: int
    professional_id: int
    date: date
    start_time: time
    status: str = "Confirmado" # Default status
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    customer_id: Optional[int] = None
    service_id: Optional[int] = None
    professional_id: Optional[int] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    customer: CustomerResponse # Retorna o objeto completo do cliente
    service: ServiceResponse
    professional: ProfessionalResponse
    class Config:
        from_attributes = True

# Anamnesis Template
class AnamnesisTemplateFieldBase(BaseModel):
    key: str
    label: str
    field_type: str # 'text', 'textarea', 'radio', 'select'
    options: Optional[List[str]] = None
    order: int = 0

class AnamnesisTemplateFieldCreate(AnamnesisTemplateFieldBase):
    pass

class AnamnesisTemplateFieldResponse(AnamnesisTemplateFieldBase):
    id: int
    class Config:
        from_attributes = True

# Anamnesis Record
class AnamnesisRecordBase(BaseModel):
    appointment_id: int
    customer_id: int
    record_date: date
    data: Dict[str, Any] # Dicionário flexível para os dados da anamnese

class AnamnesisRecordCreate(AnamnesisRecordBase):
    pass

class AnamnesisRecordUpdate(AnamnesisRecordBase):
    # Para update, o appointment_id e customer_id geralmente não mudam, mas o 'data' sim
    data: Dict[str, Any]

class AnamnesisRecordResponse(AnamnesisRecordBase):
    id: int
    customer: CustomerResponse # Inclui detalhes do cliente
    appointment: AppointmentResponse # Inclui detalhes do agendamento
    class Config:
        from_attributes = True

# Opportunity
class OpportunityBase(BaseModel):
    title: str = Field(..., min_length=3)
    customer_id: int
    value: float = Field(..., ge=0)
    stage: str = "Lead" # Default stage

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(OpportunityBase):
    title: Optional[str] = None
    customer_id: Optional[int] = None
    value: Optional[float] = None
    stage: Optional[str] = None

class OpportunityResponse(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: datetime
    customer: CustomerResponse # Retorna o objeto completo do cliente
    class Config:
        from_attributes = True

# SystemTag
class SystemTagBase(BaseModel):
    name: str = Field(..., min_length=2)
    color: Optional[str] = "bg-gray-400"

class SystemTagCreate(SystemTagBase):
    pass

class SystemTagUpdate(SystemTagBase):
    name: Optional[str] = None
    color: Optional[str] = None

class SystemTagResponse(SystemTagBase):
    id: int
    class Config:
        from_attributes = True

# Conversation
class MessageContent(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None
    caption: Optional[str] = None
    duration: Optional[str] = None
    name: Optional[str] = None
    size: Optional[str] = None

class MessageBase(BaseModel):
    sender: str # "clinic", "customer"
    message_type: str = "text" # "text", "image", "audio", "file"
    content: MessageContent # Usando o schema MessageContent para o conteúdo dinâmico
    timestamp: datetime = Field(default_factory=datetime.now)

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    customer_id: int
    unread_count: int = 0

class ConversationCreate(ConversationBase):
    # Na criação, talvez só precise do customer_id
    pass

class ConversationUpdate(ConversationBase):
    unread_count: Optional[int] = None
    last_message_at: Optional[datetime] = None

class ConversationResponse(ConversationBase):
    id: int
    last_message_at: datetime
    customer: CustomerResponse # Inclui dados do cliente associado
    messages: List[MessageResponse] = [] # Carrega as últimas mensagens, ou todas
    class Config:
        from_attributes = True

# ClinicInfo
class ClinicInfoBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    working_hours: Optional[str] = None

class ClinicInfoCreate(ClinicInfoBase):
    pass

class ClinicInfoUpdate(ClinicInfoBase):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    working_hours: Optional[str] = None

class ClinicInfoResponse(ClinicInfoBase):
    id: int
    class Config:
        from_attributes = True
