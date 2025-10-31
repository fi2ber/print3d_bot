from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(20))
    language = Column(String(2), default='ru')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(telegram_id='{self.telegram_id}', username='{self.username}')>"

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    username = Column(String(100))
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    description = Column(Text)
    file_path = Column(String(500))
    service_type = Column(String(20), nullable=False)  # print, modeling, scanning
    material = Column(String(50))
    color = Column(String(50))
    strength_accuracy = Column(String(100))
    usage_temp = Column(String(50))
    quantity = Column(Integer, default=1)
    deadline = Column(String(100))
    location = Column(String(200))
    language = Column(String(2), default='ru')
    status = Column(String(20), default='new')
    manager_contact = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id='{self.user_id}', service_type='{self.service_type}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'name': self.name,
            'phone': self.phone,
            'description': self.description,
            'file_path': self.file_path,
            'service_type': self.service_type,
            'material': self.material,
            'color': self.color,
            'strength_accuracy': self.strength_accuracy,
            'usage_temp': self.usage_temp,
            'quantity': self.quantity,
            'deadline': self.deadline,
            'location': self.location,
            'language': self.language,
            'status': self.status,
            'manager_contact': self.manager_contact,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Database:
    def __init__(self, db_url='sqlite:///database/print3d.db'):
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(db_url.replace('sqlite:///', ''))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
    
    def add_user(self, telegram_id, username=None, first_name=None, last_name=None, phone_number=None, language='ru'):
        session = self.get_session()
        try:
            user = User(
                telegram_id=str(telegram_id),
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                language=language
            )
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user(self, telegram_id):
        session = self.get_session()
        try:
            return session.query(User).filter_by(telegram_id=str(telegram_id)).first()
        finally:
            session.close()
    
    def update_user_language(self, telegram_id, language):
        session = self.get_session()
        try:
            user = session.query(User).filter_by(telegram_id=str(telegram_id)).first()
            if user:
                user.language = language
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def add_order(self, **kwargs):
        session = self.get_session()
        try:
            order = Order(**kwargs)
            session.add(order)
            session.commit()
            return order
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_orders(self, user_id):
        session = self.get_session()
        try:
            return session.query(Order).filter_by(user_id=str(user_id)).order_by(Order.created_at.desc()).all()
        finally:
            session.close()
    
    def get_order(self, order_id):
        session = self.get_session()
        try:
            return session.query(Order).filter_by(id=order_id).first()
        finally:
            session.close()
    
    def update_order_status(self, order_id, status, manager_contact=None):
        session = self.get_session()
        try:
            order = session.query(Order).filter_by(id=order_id).first()
            if order:
                order.status = status
                if manager_contact:
                    order.manager_contact = manager_contact
                session.commit()
                return order
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_all_orders(self):
        session = self.get_session()
        try:
            return session.query(Order).order_by(Order.created_at.desc()).all()
        finally:
            session.close()
    
    def get_orders_by_status(self, status):
        session = self.get_session()
        try:
            return session.query(Order).filter_by(status=status).order_by(Order.created_at.desc()).all()
        finally:
            session.close()
