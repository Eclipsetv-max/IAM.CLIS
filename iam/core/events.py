# -*- coding: utf-8 -*-
"""
IAM Events - Sistema de eventos Pub/Sub
Inspirado en OpenCode: event-driven architecture con non-blocking publish
"""

import threading
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import queue


class EventType(Enum):
    """Tipos de eventos"""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    ERROR = "error"


@dataclass
class Event:
    """Evento generico"""
    type: EventType
    payload: Any
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    source: str = ""


class Broker:
    """
    Broker de eventos Pub/Sub
    Inspirado en OpenCode: non-blocking publish, auto-unsubscribe
    """
    
    def __init__(self, max_events: int = 1000, buffer_size: int = 64):
        self._subscribers: Dict[str, queue.Queue] = {}
        self._lock = threading.RLock()
        self._max_events = max_events
        self._buffer_size = buffer_size
        self._event_count = 0
        self._shutdown = False
    
    def subscribe(self, subscriber_id: str = None) -> queue.Queue:
        """Suscribirse a eventos. Retorna una cola de eventos."""
        if self._shutdown:
            raise RuntimeError("Broker has been shut down")
        
        if subscriber_id is None:
            subscriber_id = f"sub_{id(queue.Queue())}"
        
        with self._lock:
            event_queue = queue.Queue(maxsize=self._buffer_size)
            self._subscribers[subscriber_id] = event_queue
            return event_queue
    
    def unsubscribe(self, subscriber_id: str):
        """Desuscribirse"""
        with self._lock:
            if subscriber_id in self._subscribers:
                del self._subscribers[subscriber_id]
    
    def publish(self, event_type: EventType, payload: Any, source: str = ""):
        """
        Publicar evento a todos los suscriptores (non-blocking)
        Si un suscriptor esta lleno, el evento se descarta (no bloquea)
        """
        if self._shutdown:
            return
        
        event = Event(
            type=event_type,
            payload=payload,
            source=source
        )
        
        with self._lock:
            self._event_count += 1
            # Copiar lista de suscriptores para evitar problemas de concurrencia
            subscribers = list(self._subscribers.values())
        
        # Publicar non-blocking
        for sub_queue in subscribers:
            try:
                sub_queue.put_nowait(event)
            except queue.Full:
                # Suscriptor lleno, descartar evento (no bloquear)
                pass
    
    def get_event_count(self) -> int:
        """Obtener numero total de eventos publicados"""
        return self._event_count
    
    def get_subscriber_count(self) -> int:
        """Obtener numero de suscriptores activos"""
        with self._lock:
            return len(self._subscribers)
    
    def shutdown(self):
        """Cerrar el broker"""
        self._shutdown = True
        with self._lock:
            for sub_queue in self._subscribers.values():
                try:
                    sub_queue.put_nowait(None)  # Senal de cierre
                except queue.Full:
                    pass
            self._subscribers.clear()


class EventManager:
    """
    Gestor central de eventos
    Proporciona brokers para diferentes tipos de eventos
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # Brokers para diferentes dominios
        self.sessions = Broker()
        self.messages = Broker()
        self.files = Broker()
        self.permissions = Broker()
        self.agent = Broker()
        self.system = Broker()
        
        # Registro de handlers
        self._handlers: Dict[str, List[Callable]] = {}
    
    def on(self, event_name: str, handler: Callable):
        """Registrar handler para un evento"""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
    
    def off(self, event_name: str, handler: Callable):
        """Remover handler"""
        if event_name in self._handlers:
            self._handlers[event_name] = [
                h for h in self._handlers[event_name] if h != handler
            ]
    
    def emit(self, event_name: str, data: Any = None):
        """Emitir evento a handlers registrados"""
        if event_name in self._handlers:
            for handler in self._handlers[event_name]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error in event handler {event_name}: {e}")
    
    def shutdown(self):
        """Cerrar todos los brokers"""
        self.sessions.shutdown()
        self.messages.shutdown()
        self.files.shutdown()
        self.permissions.shutdown()
        self.agent.shutdown()
        self.system.shutdown()


# Instancia global
events = EventManager()


# ==================== DECORADORES ====================

def on_event(broker_name: str, event_type: EventType = None):
    """
    Decorador para registrar handler de eventos
    
    Uso:
        @on_event("sessions", EventType.CREATED)
        def on_session_created(event: Event):
            print(f"Session created: {event.payload}")
    """
    def decorator(func):
        broker = getattr(events, broker_name, None)
        if broker:
            def wrapper(event: Event):
                if event_type is None or event.type == event_type:
                    func(event)
            
            # Crear suscriptor
            sub_id = f"{func.__module__}.{func.__name__}"
            event_queue = broker.subscribe(sub_id)
            
            # Escuchar en background
            def listener():
                while True:
                    try:
                        event = event_queue.get(timeout=1)
                        if event is None:  # Senal de cierre
                            break
                        wrapper(event)
                    except queue.Empty:
                        continue
                    except Exception as e:
                        print(f"Event listener error: {e}")
            
            thread = threading.Thread(target=listener, daemon=True)
            thread.start()
        
        return func
    return decorator
