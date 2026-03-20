# TickPay — Manual de Usuario Completo
### Guía Oficial de la Plataforma · Versión 1.0 · 2026

---

> [!IMPORTANT]
> Este manual cubre el flujo de trabajo **completo** de la plataforma TickPay, desde el primer acceso hasta la integración avanzada de agentes autónomos. Léelo de principio a fin antes de comenzar a integrar.

---

## Tabla de Contenidos

1. [¿Qué es TickPay?](#1-qué-es-tickpay)
2. [Arquitectura General](#2-arquitectura-general)
3. [Acceso y Autenticación](#3-acceso-y-autenticación)
4. [Dashboard Principal](#4-dashboard-principal)
5. [Balances y Fondos (Liquidity & Funding)](#5-balances-y-fondos)
6. [Transacciones](#6-transacciones)
7. [Tarjetas Virtuales (Cards)](#7-tarjetas-virtuales-cards)
8. [Developer Console — Claves API y Agentes](#8-developer-console--claves-api-y-agentes)
9. [Configuración del Workspace (Settings)](#9-configuración-del-workspace-settings)
10. [Webhooks — Integración Asíncrona](#10-webhooks--integración-asíncrona)
11. [SDK de Node.js — Integración Completa](#11-sdk-de-nodejs--integración-completa)
12. [Primitivas Agénticas — Escrow y Swarm Wallets](#12-primitivas-agénticas--escrow-y-swarm-wallets)
13. [SLA Market Orderbook](#13-sla-market-orderbook)
14. [Sistema de Cuarentena (Human-in-the-Loop)](#14-sistema-de-cuarentena-human-in-the-loop)
15. [Panel de Administración (Admin Hub)](#15-panel-de-administración-admin-hub)
16. [Páginas Públicas e Infraestructura](#16-páginas-públicas-e-infraestructura)
17. [Flujos de Trabajo Completos (End-to-End)](#17-flujos-de-trabajo-completos-end-to-end)
18. [Seguridad y Mejores Prácticas](#18-seguridad-y-mejores-prácticas)
19. [Glosario](#19-glosario)

---

## 1. ¿Qué es TickPay?

TickPay es una **infraestructura de pagos autónoma de máquina a máquina (M2M)** diseñada para agentes de inteligencia artificial. Permite que tus bots, scripts o servicios de IA ejecuten micropagos en tiempo real, gestionen fondos en escrow condicional, emitan tarjetas virtuales y participen en un mercado descentralizado de servicios (SLA Orderbook).

**Casos de uso principales:**
- Un agente de IA que paga automáticamente por tokens de LLM (GPT-4, etc.)
- Un sistema de e-commerce que bloquea fondos en escrow hasta confirmar entrega física
- Un enjambre de agentes (Swarm) que comparte una tesorería multifirma (Multisig)
- Un bot que contrata servicios de Render 3D o scraping de datos y paga por resultado

---

## 2. Arquitectura General

```
┌─────────────────────────────────────────────────┐
│                  FRONTEND (SPA)                  │
│  Landing ─ Login ─ Dashboard ─ Balances ─ Cards │
│  Transactions ─ Developer Console ─ Settings     │
└────────────────────┬────────────────────────────┘
                     │ REST API (Bearer Token)
┌────────────────────▼────────────────────────────┐
│               API GATEWAY LAYER                  │
│  Router ─ Middleware ─ Services ─ Webhooks       │
└──────┬──────────────────────────┬───────────────┘
       │                          │
┌──────▼──────┐          ┌────────▼────────┐
│  Ledger DB  │          │   Cache Layer   │
│             │          │                 │
└─────────────┘          └─────────────────┘
```

**URLs y Rutas de la plataforma:**

| Tipo | Ruta | Descripción |
|------|------|-------------|
| Pública | `/` | Landing Page |
| Pública | `/login` | Inicio de sesión |
| Pública | `/docs-intro` | Documentación pública |
| Pública | `/sdk` | Página del SDK |
| Pública | `/api` | Referencia de API |
| Pública | `/architecture` | Topología del sistema |
| Pública | `/infrastructure` | Mapa de infraestructura |
| Pública | `/nodes` | Monitor de nodos L2 |
| **Protegida** | `/dashboard` | Panel principal (requiere login) |
| **Protegida** | `/balances` | Gestión de fondos |
| **Protegida** | `/transactions` | Historial de transacciones |
| **Protegida** | `/cards` | Tarjetas virtuales |
| **Protegida** | `/developers/api-keys` | Developer Console |
| **Protegida** | `/settings` | Configuración del workspace |
| **Protegida** | `/docs` | Documentación interna |
| 🔒 **Admin** | *(acceso restringido)* | Panel de administración global |

---

## 3. Acceso y Autenticación

### 3.1 Registro e Inicio de Sesión

**Pre-requisito:** Una cuenta de correo electrónico válida.

**Pasos:**

1. Navega a la URL de la plataforma (ej: `https://your-tickpay-domain.com`)
2. Haz clic en **"Get Started"** o navega directamente a `/login`
3. En la pantalla de Login, tienes dos opciones:
   - **Correo + Contraseña:** Ingresa tu email y contraseña registrados
   - **Google OAuth:** Haz clic en el botón de Google si está disponible
4. El sistema utiliza un proveedor de autenticación seguro para gestionar sesiones
5. Tras autenticarte, serás redirigido automáticamente a `/dashboard`

> [!WARNING]
> Las cuentas con permisos de administrador son redirigidas automáticamente a su panel exclusivo. Esta es una separación estricta de roles.

### 3.2 Sesión y Protección de Rutas

- Todas las rutas bajo `/dashboard`, `/balances`, `/transactions`, `/cards`, `/developers/api-keys`, `/settings`, y `/docs` están protegidas por autenticación
- Si intentas acceder sin sesión activa, serás redirigido a `/login`
- La sesión se mantiene de forma segura siguiendo mejores prácticas contra ataques XSS

---

## 4. Dashboard Principal

**Ruta:** `/dashboard`

El Dashboard es el **centro de control** de tu organización. Muestra métricas globales en tiempo real y acceso rápido a todas las funciones.

### 4.1 Métricas del Header (Hero Metrics)

Al ingresar al dashboard verás:

| Métrica | Descripción |
|---------|-------------|
| **Total Balance** | Saldo líquido disponible para que tus agentes gasten ahora mismo |
| **M2M Reserves / TVL** | Fondos temporalmente "congelados" en contratos inteligentes (escrow pendiente, pagos condicionales) |
| **Active Agents** | Número de agentes conectados activamente a la red |
| **API Requests** | Total de transacciones procesadas y registradas en el ledger global |

### 4.2 Botones de Acción Rápida

Desde el header del dashboard:

#### ▶ "Add Funds" (Agregar Fondos)
1. Haz clic en el botón blanco **"Add funds"**
2. Se abre un modal con un campo de monto en USD
3. Ingresa el monto de depósito (mínimo $10)
4. Haz clic en **"Deposit to Vault"**
5. El saldo se reflejará en tu balance global

#### ▶ "Send Payment" (Enviar Pago)
1. Haz clic en **"Send payment"**
2. Se abre el modal de **Send Payment**
3. Completa los campos:
   - **Target Agent Node:** El ID del nodo destino (ej: `node_a1b2c3d4`)
   - **Execution Amount:** El monto a enviar en USD
4. Haz clic en **"Authorize & Emmit"**
5. El sistema genera una firma criptográfica y enruta el pago

> [!CAUTION]
> Los fondos enviados son **no reversibles** una vez que se alcanza el consenso criptográfico. Siempre verifica el ID del nodo destino antes de confirmar.

### 4.3 Gráfico de Métricas

- El gráfico central (`MetricsChart`) muestra el **volumen de transacciones de los últimos 7 días** como serie temporal
- Los datos provienen del ledger L2 en tiempo real
- Hover sobre el gráfico para ver valores exactos por día

### 4.4 Cuadro Educativo — Entendiendo tu Ledger

El dashboard incluye un cuadro informativo azul que explica:
- **Total Balance** = dinero líquido disponible ahora
- **M2M Reserves/TVL** = fondos bloqueados en contratos (no disponibles todavía)

### 4.5 Active Payment Streams (Streams en Vivo)

En la sección inferior izquierda verás los **canales de pago activos**:
- Muestra pares de agentes conectados en tiempo real (ej: `ag_buyer_001 → ag_compute_node`)
- Cada stream muestra el monto acumulado actual y el **Escrow Lock** (fondos bloqueados como garantía)
- El indicador verde pulsante indica que el stream está activo

### 4.6 SLA Market Orderbook (Vista Rápida)

En la sección inferior derecha se muestra el **libro de órdenes del mercado**:
- Cada fila es un tipo de servicio ofrecido en la red (ej: `LLM.GPT4.Completion`, `Render.3D.Blender`)
- **Bid** = precio máximo que el comprador está dispuesto a pagar
- **Ask** = precio mínimo que el proveedor acepta
- Cuando `Bid ≥ Ask`, el motor de matching ejecuta el acuerdo automáticamente (indicado con badge "Match")

### 4.7 Recibo de Transacción (Execution Receipt)

Al hacer clic en cualquier transacción de la tabla "Recent Activity", se abre un **drawer lateral** con:
- Monto de liquidación
- Estado de la transacción
- Agent Target (nodo destino)
- Block Timestamp (marca de tiempo del bloque)
- Transaction Hash (hash único de la transacción)
- Raw Ledger Payload (payload JSON completo de la transacción)

---

## 5. Balances y Fondos

**Ruta:** `/balances`

Esta pantalla es tu centro de **gestión de liquidez**. Controlas aquí cuánto dinero tienen disponible cada uno de tus agentes.

### 5.1 Tres Paneles Superiores

#### Panel 1: Global Fiat Pool
- Muestra tu **balance total disponible** en USD
- Es el dinero que tus agentes pueden gastar en este momento
- APY visualizado (rendimiento actual)

#### Panel 2: Yield Engine / Treasury Vault
- Muestra el balance acumulado de **tesorería** de todos tus agentes combinados
- Muestra el APY compuesto actual del vault (ej: +5.50% APY)
- Este saldo crece automáticamente según el rendimiento

#### Panel 3: Add Funds — Recarga Rápida
1. Selecciona un monto predefinido: **$50, $100, $250, $500**
   - Haz clic en el botón del monto deseado (se resalta en verde)
2. O ingresa un monto personalizado en el campo **"custom amount (USD)"**
3. Haz clic en **"Proceed to Checkout"**
4. El sistema iniciará el proceso de depósito

### 5.2 Agent Budget Allocation (Tabla de Asignación)

Esta tabla muestra todos tus agentes registrados con sus métricas de gasto:

| Columna | Descripción |
|---------|-------------|
| **Agent ID** | Identificador único del agente (ej: `ag_buyer_001`) |
| **Status** | `Active` (verde) o `Paused` (ámbar) |
| **Daily Limit** | Límite de gasto diario asignado a ese agente |
| **Spent Today** | Cuánto ha gastado el agente hoy |
| **Utilization** | Barra de progreso: verde si < 80%, ámbar si > 80% |

> [!TIP]
> Los agentes con badge **KYA ✓** (Know Your Agent) tienen verificación de identidad ZK completada, lo que les permite operar con límites más altos.

Para gestionar los límites de cada agente, haz clic en **"Manage Limits"** (arriba a la derecha de la tabla).

---

## 6. Transacciones

**Ruta:** `/transactions`

El historial completo de todas las operaciones ejecutadas en el ledger global.

### 6.1 Lista de Transacciones

Cada transacción muestra:
- **Descripción:** Tipo de pago (ej: "API Payment") y el ID del agente origen
- **Fecha:** Timestamp de cuando se liquidó en el ledger
- **Status:** Estado de la transacción (`completed`, `failed`, `pending`)
- **Amount:** Monto en USD

### 6.2 Filtros y Exportación

- **Búsqueda:** Usa el buscador circular para filtrar transacciones por texto
- **Filtros avanzados:** Haz clic en el ícono de filtro (embudo) para filtrar por estado, fecha, etc.
- **Exportar CSV:** Haz clic en el ícono de descarga para generar un export en CSV

### 6.3 Ver Detalle de Transacción

Haz clic en cualquier fila de la tabla para abrir el **Execution Receipt drawer** con todos los detalles criptográficos.

---

## 7. Tarjetas Virtuales (Cards)

**Ruta:** `/cards`

Emite y gestiona tarjetas virtuales PCI-DSS vinculadas al balance de tu organización.

### 7.1 Prerrequisito para Emitir Tarjetas

> [!IMPORTANT]
> Para poder emitir tarjetas virtuales, **primero debes** crear una API Key con el scope `cards:issue` activado (ver sección 8). Sin este permiso, el sistema rechazará cualquier intento de emisión.

### 7.2 Emitir una Tarjeta Virtual

1. Navega a `/cards`
2. Haz clic en **"Issue New Card"** (o similar)
3. Define los parámetros:
   - **Límite de la tarjeta** (en USD)
   - **Agente asignado** (qué agente controlará esta tarjeta)
   - **Expiración** y configuraciones adicionales
4. Confirma la emisión
5. La tarjeta aparecerá en el listado con su número, CVV enmascarado y fecha de expiración

> [!WARNING]
> Las tarjetas emitidas están vinculadas al saldo global de tu organización. El scope `cards:issue` se clasifica como **CRÍTICO** — solo otórgalo a claves API absolutamente confiables.

---

## 8. Developer Console — Claves API y Agentes

**Ruta:** `/developers/api-keys`

Esta es la sección más **importante** para developers. Aquí gestionas tus claves API y monitorizas la salud de tus integraciones.

### 8.1 ¿Qué es una API Key en TickPay?

Una API Key es el **"documento de identidad"** de tu agente. Sin ella, tu agente no puede:
- Ejecutar pagos
- Leer el estado del ledger
- Emitir tarjetas virtuales
- Interactuar con ningún endpoint del backend

Las claves se distinguen por su prefijo:
- `sk_test_...` → Clave de pruebas. No mueven fondos reales (ideal para desarrollo)
- `sk_live_...` → Clave de producción. Cada llamada es **inmutable y en tiempo real**

### 8.2 Generar tu Primera API Key (Flujo Básico)

1. Ve a `/developers/api-keys`
2. En el panel **"Live Secret Key"** (izquierda), haz clic en **"Generate Live API Key"**
3. El sistema calcula entropía criptográfica y muestra la clave generada
4. **⚠ COPIA LA CLAVE INMEDIATAMENTE** — solo se muestra una vez completa
5. Usa los botones de ojo (👁) para revelarla y de copia para copiarla al portapapeles

> [!CAUTION]
> Por seguridad bancaria estándar (PCI-DSS), TickPay **nunca** guarda la clave master en localStorage o sessionStorage para mitigar ataques XSS. Si pierdes la clave deberás generar una nueva. La clave anterior quedará invalidada automáticamente.

### 8.3 Quickstart Code Snippet

En el panel derecho del Developer Console verás un ejemplo de código **Node.js/TypeScript** listo para usar:

```typescript
// 1. Instalar via NPM
npm install @tickpay/agent-sdk

// 2. Inicializar el cliente
import { TickPay } from '@tickpay/agent-sdk';
const tickpay = new TickPay('sk_live_TU_CLAVE_AQUI');

// 3. Ejecutar un pago autónomo
await tickpay.emmitPayment({
  target: 'node_alpha_x',
  amount: 25.50
});
```

Si ya generaste tu clave, el snippet la mostrará **precargada automáticamente** en el código de ejemplo.

> [!TIP]
> El SDK no es obligatorio. Puedes usar `fetch()` directamente a la REST API. Sin embargo, el SDK incluye **reintentos automáticos con Exponential Backoff** y autocompletado nativo de TypeScript, ahorrando horas de desarrollo.

### 8.4 Watchdog Telemetry Logs

En la sección inferior del Developer Console verás la tabla de **logs del Watchdog**. Estos logs muestran el historial de llamadas a tu endpoint:

| Columna | Descripción |
|---------|-------------|
| **Timestamp** | Fecha y hora exacta de la llamada |
| **Event ID** | Identificador único del evento (ej: `wh_ex123`) |
| **Method/Endpoint** | Método HTTP y endpoint llamado (ej: `POST /v1/agent/action`) |
| **Status** | `200 OK` (éxito) o `403 QUARANTINED` (rechazado) |
| **Latency** | Tiempo de respuesta en milisegundos |

**Lógica de reintentos del Watchdog:**
- Si TickPay no recibe un `200 OK` de tu servidor en el tiempo establecido, aborta el webhook
- Reintenta automáticamente con backoff exponencial durante un período extendido

---

## 9. Configuración del Workspace (Settings)

**Ruta:** `/settings`

Centro de configuración de tu organización. Dividido en secciones claramente diferenciadas.

### 9.1 Company Details (Perfil de la Empresa)

1. Ve a `/settings`
2. En la sección **"Company Details"**, actualiza:
   - **Company Name:** Nombre de tu empresa u organización
   - **Contact Email:** Email de facturación o contacto principal
3. Haz clic en **"Save"** para guardar los cambios

### 9.2 Team Management (Gestión de Equipo)

Invita a colegas a tu workspace con diferentes niveles de acceso.

**Roles disponibles:**

| Rol | Acceso |
|-----|--------|
| **Admin** | Acceso completo: puede generar claves, gestionar equipo, ver todo |
| **Developer** | Puede generar y revocar API Keys, ver logs y transacciones |
| **Billing** | Solo puede ver balances y gestionar métodos de pago |

**Pasos para invitar:**
1. En la sección "Team Management", ingresa el **correo del colega** en el campo de email
2. Selecciona el **rol** en el dropdown
3. Haz clic en **"Invite Member"**
4. El colega recibirá un email de invitación

Para **remover** a un miembro, hover sobre su fila y haz clic en el ícono de basura (🗑) que aparece.

### 9.3 API Keys Management (Gestión Avanzada de Claves)

Esta sección en Settings es la interfaz **avanzada** para gestionar múltiples claves API con control de scopes (RBAC).

#### Flujo completo para crear una API Key con Scopes:

**Paso 1: Abrir el configurador**
1. En la sección "API Keys", haz clic en **"Configure New Key"**
2. Se abre el modal de configuración de scopes

**Paso 2: Seleccionar permisos (Scopes RBAC)**

| Scope | Nivel | Descripción |
|-------|-------|-------------|
| `transactions:read` | Default | Siempre activo. Permite leer historial y métricas del ledger |
| `transactions:write` | Nivel 2 | Permite ejecutar pagos y autorizar escrow en el L2 Ledger |
| `cards:issue` | 🔴 CRÍTICO | Permite emitir tarjetas PCI-DSS virtuales. ¡Úsalo con extremo cuidado! |

3. Marca los checkboxes de los scopes que necesitas
4. Haz clic en **"Provision Key with Scopes"**

**Paso 3: Guardar la clave**
1. Se genera la clave y se muestra una sola vez
2. Aparece el modal de guardado con el campo **"Name your key"**
3. Dale un nombre descriptivo (ej: `Production AWS Bot`, `Staging Agent v2`)
4. **Copia la clave** haciendo clic en "Copy Key"
5. Haz clic en **"I have copied it, Save to List"**
6. La clave aparecerá en el listado con sus scopes y fecha de creación

#### Gestionar claves existentes:

En el listado de claves puedes:
- **👁 Revelar/Ocultar** la clave (toggle de visibilidad)
- **📋 Copiar** la clave al portapapeles
- **🗑 Revocar** la clave (hover sobre la fila para ver el botón)

#### Ver ejemplos de integración:
Haz clic en **"View DX Integration Examples"** para abrir un modal con el snippet de código SDK listo para usar con tu clave activa.

### 9.4 Danger Zone (Zona de Peligro)

Al final de la página de Settings, hay dos acciones irreversibles:

- **"Revoke All API Keys":** Invalida **todas** las claves activas. Requiere autenticación multifactor (MFA). Tu red de agentes quedará sin acceso inmediatamente.
- **"Delete Workspace":** Elimina toda la organización. Actualmente bloqueado por protocolos de seguridad.

> [!CAUTION]
> Revocar todas las claves es una acción de **emergencia**. Úsala solo si sospechas de una brecha de seguridad. Todos tus agentes dejarán de funcionar hasta que generes e implementes nuevas claves.

---

## 10. Webhooks — Integración Asíncrona

**Ruta:** `/settings` → Sección "Developer Webhooks"

Los webhooks son el mecanismo por el cual TickPay **notifica a tu servidor** cuando ocurren eventos asíncronos (pagos completados, fondos de escrow liberados, etc.).

### 10.1 ¿Por qué son necesarios los Webhooks?

Muchas operaciones en TickPay son **asíncronas**: cuando un agente inicia un pago, puede tomar unos momentos para que la red L2 confirme el bloque. En lugar de que tu servidor haga polling constante, TickPay envía un `HTTP POST` a tu endpoint cuando el evento ocurre.

### 10.2 Configurar tu Webhook URL

1. Ve a `/settings`
2. En la sección **"Developer Webhooks"**, encuentra el campo **"Webhook URL"**
3. Ingresa la URL de tu servidor (ej: `https://api.tuempresa.com/webhooks/tickpay`)
4. Haz clic en **"Save Endpoint"**

### 10.3 Verificar Webhooks con HMAC-SHA256

Para garantizar que los webhooks realmente provienen de TickPay (y no de un atacante):

1. En Settings, copia el **Webhook Secret** (`whsec_...`) haciendo clic en el ícono de copiar
2. En tu servidor, implementa la verificación de firma:

```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const expectedSig = hmac.update(payload).digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSig)
  );
}
```

3. Cada request de TickPay incluirá un header con la firma. Si no coincide, **rechaza el request**.

### 10.4 Tu Servidor debe Responder

- **Tiempo máximo de respuesta:** En caso de no recibir respuesta, TickPay aborta y reintenta automáticamente
- **Respuesta esperada:** `HTTP 200 OK`
- **Política de reintentos:** TickPay implementa un sistema automático de reintentos con backoff exponencial durante un período extendido

---

## 11. SDK de Node.js — Integración Completa

El SDK oficial de TickPay (`@tickpay/agent-sdk`) está disponible vía NPM.

### 11.1 Instalación

```bash
npm install @tickpay/agent-sdk
```

### 11.2 Inicialización

```typescript
import { TickPay } from '@tickpay/agent-sdk';

// Nunca hardcodees la clave. Usa variables de entorno.
const tickpay = new TickPay(process.env.TICKPAY_SECRET_KEY);
```

### 11.3 Ejecutar un Pago (emmitPayment)

```typescript
const result = await tickpay.emmitPayment({
  target: 'node_alpha_x',  // ID del nodo destino
  amount: 25.50            // Monto en USD
});
```

### 11.4 Crear Transacción con Descripción

```typescript
await tickpay.transactions.create({
  amount: 0.05,
  currency: 'USD',
  recipientId: 'agt_5c4a8f9b2d11e0f9',
  description: 'API Usage: 10k tokens'
});
```

### 11.5 Uso sin SDK (fetch directo)

```javascript
const response = await fetch('https://api.tickpay.io/v1/agent/action', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.TICKPAY_SECRET_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    target: 'node_alpha_x',
    amount: 25.50
  })
});
```

---

## 12. Primitivas Agénticas — Escrow y Swarm Wallets

Estas son las funciones más avanzadas de TickPay, diseñadas para casos de uso M2M complejos.

### 12.1 Programmable Escrow (Escrow Programable)

El escrow es un **contrato de custodia condicional**. Los fondos se bloquean y solo se liberan cuando se cumple una condición específica.

**Caso de uso:** Un agente comprador paga por un servicio de render 3D. Los fondos quedan bloqueados. Cuando el render se completa y el archivo es validado, los fondos se liberan automáticamente al agente proveedor.

**Widget en Dashboard:**
- Muestra fondos actuales bloqueados en contratos abiertos
- Número de contratos activos
- Botón "View Escrow Contracts" para ver el detalle

**Via API (endpoints del backend):**
- `POST /v1/escrow/create` — Crear un contrato de escrow
- `POST /v1/escrow/resolve` — Resolver (liberar o reembolsar) un contrato

> [!NOTE]
> Los contratos de escrow usan verificación criptográfica. Una vez creado un escrow, ninguna de las partes puede modificar unilateralmente las condiciones.

### 12.2 Swarm Wallets — Tesorería Multifirma

Un **Swarm Wallet** es una billetera compartida por múltiples agentes que requiere N-de-M firmas para ejecutar transacciones. Es equivalente a una cuenta bancaria con múltiples autorizadores.

**Widget en Dashboard:**
- Muestra el balance total de la tesorería del enjambre
- Número de propuestas pendientes de firma
- Botón "Review Pending Proposals" para aprobar o rechazar propuestas

**Flujo de una transacción Swarm:**
1. Un agente propone una transacción (ej: `ag_buyer_001` quiere pagar $500)
2. La propuesta aparece como "Pending Signature"
3. Los demás agentes autorizados deben firmar (según el threshold N-de-M)
4. Cuando se alcanza el umbral, la transacción se ejecuta automáticamente

---

## 13. SLA Market Orderbook

**Ubicación:** Dashboard → Panel inferior derecho

El Orderbook es el **mercado descentralizado** de servicios en la red TickPay. Agentes compradores y proveedores publican bids y asks para servicios específicos.

**Servicios disponibles (ejemplos):**

| Servicio | Descripción |
|----------|-------------|
| `LLM.GPT4.Completion` | Completaciones de texto con GPT-4 |
| `Render.3D.Blender` | Renderizado 3D en servidores remotos |
| `Data.Scrape.Twitter` | Scraping de datos de redes sociales |

**Columnas del Orderbook:**

| Columna | Descripción |
|---------|-------------|
| **Bid (Max Price)** | El precio máximo que el comprador acepta pagar |
| **Ask (Min Price)** | El precio mínimo que el proveedor acepta recibir |
| **Match badge** | Aparece cuando `Bid ≥ Ask` y el motor ejecuta el acuerdo |

El **Matching Engine** opera en tiempo real (indicado por el punto pulsante). Cuando encuentra un match, ejecuta el contrato automáticamente sin intervención humana.

---

## 14. Sistema de Cuarentena (Human-in-the-Loop)

**Ubicación:** Dashboard → Banner rojo (aparece solo cuando hay anomalías)

TickPay incluye un sistema de **detección de anomalías**. Cuando un agente intenta ejecutar un pago que es clasificado como "Alto Riesgo" o "Fondos Insuficientes", la transacción queda en estado `FAILED` y se muestra un banner de alerta rojo en el Dashboard.

### 14.1 Cómo Responder a una Anomalía

Cuando aparece el banner de cuarentena:

**Opción A: Rechazar y Bloquear**
1. Haz clic en **"Reject & Lock"** (botón rojo con borde)
2. La transacción es explícitamente rechazada
3. El agente queda bloqueado temporalmente
4. Se registra el evento en los logs con resolución `rejected`

**Opción B: Acknowledge (Reconocer)**
1. Haz clic en **"Acknowledge"** (botón rojo sólido)
2. La anomalía es reconocida y el banner desaparece
3. Los logs muestran resolución `approved`

> [!NOTE]
> Este mecanismo es conocido como "Human-in-the-Loop" (HITL) — garantiza que siempre haya supervisión humana en transacciones de alto riesgo, incluso en sistemas completamente automatizados.

---

## 15. Panel de Administración (Admin Hub)

**Ruta:** `/admin` (y sub-rutas)

> [!WARNING]
> El panel de administración es **exclusivo** para cuentas con rol de administrador. Si intentas acceder con una cuenta sin privilegios suficientes, serás redirigido silenciosamente al dashboard. No existe navegación visible hacia esta sección desde el UI normal — es una ruta protegida con control de acceso basado en roles (RBAC).

El Admin Hub tiene su propio layout visual separado, diseñado para gestión operacional de la plataforma.

### 15.1 Sub-secciones del Admin Hub

| Sección | Descripción |
|---------|-------------|
| **Dashboard** | KPIs globales de la red |
| **Usuarios** | Gestión de cuentas de usuarios |
| **Transacciones** | Vista global de operaciones en la plataforma |
| **Soporte** | Gestión de tickets de soporte |
| **Configuración** | Parámetros globales de la plataforma |

---

## 16. Páginas Públicas e Infraestructura

Estas páginas no requieren autenticación y proveen información sobre la plataforma:

| Ruta | Página | Contenido |
|------|--------|-----------|
| `/` | **Landing Page** | Presentación comercial de TickPay |
| `/docs-intro` | **Documentation** | Introducción a la documentación técnica |
| `/sdk` | **Core SDK** | Documentación del SDK de Node.js |
| `/architecture` | **Architecture** | Diagrama y explicación de la topología del sistema |
| `/api` | **API Reference** | Referencia completa de todos los endpoints REST |
| `/infrastructure` | **Infrastructure Map** | Mapa visual de la infraestructura de red |
| `/nodes` | **Nodes Monitor** | Estado en tiempo real de los nodos L2 activos |
| `/about` | **About Us** | Información corporativa |
| `/security` | **Security** | Auditorías de seguridad e información de compliance |
| `/contact` | **Contact Sales** | Formulario de contacto para ventas |
| `/terms` | **Terms of Service** | Términos y condiciones |
| `/privacy` | **Privacy Policy** | Política de privacidad |
| `/compliance` | **Compliance** | Información de cumplimiento regulatorio |

---

## 17. Flujos de Trabajo Completos (End-to-End)

### Flujo A: Integrar un Agente Autónomo de Pago por Primera Vez

```
1. Registrarse en la plataforma
   └── /login → crear cuenta

2. Agregar fondos al workspace
   └── /dashboard → "Add Funds" → ingresar monto → "Deposit to Vault"

3. Generar una API Key con permisos adecuados
   └── /settings → "API Keys" → "Configure New Key"
       ├── Activar scope: transactions:read (default)
       ├── Activar scope: transactions:write (para ejecutar pagos)
       └── "Provision Key with Scopes" → copiar clave → guardar

4. Instalar el SDK en tu proyecto
   └── npm install @tickpay/agent-sdk

5. Inicializar el cliente en tu agente
   └── const tickpay = new TickPay(process.env.TICKPAY_SECRET_KEY);

6. Ejecutar el primer pago
   └── await tickpay.emmitPayment({ target: 'node_destino', amount: 1.00 });

7. Verificar en el Dashboard
   └── /dashboard → "Recent Activity" → ver la transacción

8. Configurar Webhooks para notificaciones asíncronas
   └── /settings → "Developer Webhooks" → ingresar URL → "Save Endpoint"
```

### Flujo B: Crear un Contrato de Escrow Condicional

```
1. Asegurarse de tener una API Key con scope transactions:write
   └── /settings → API Keys

2. Crear el contrato via API
   └── POST /v1/escrow/create
       {
         "buyer_agent": "ag_buyer_001",
         "seller_agent": "ag_compute_node",
         "amount": 50.00,
         "condition": "render_job_completed"
       }

3. El contrato aparece en el Dashboard
   └── /dashboard → "Programmable Escrow" widget
       ├── Fondos bloqueados: $50.00
       └── Contratos abiertos: 1

4. Cuando se cumple la condición, resolver el escrow
   └── POST /v1/escrow/resolve
       {
         "contract_id": "esc_xxxx",
         "resolution": "release"  // o "refund"
       }

5. Los fondos se transfieren al beneficiario
   └── Verificar en /transactions → nueva transacción de liquidación
```

### Flujo C: Monitorear la Salud de tu Integración

```
1. Revisar el Developer Console
   └── /developers/api-keys → sección "Watchdog Telemetry Logs"
       ├── Ver timestamps de llamadas recientes
       ├── Verificar que todos los status son "200 OK"
       └── Identificar endpoints con latencias altas

2. Revisar el Dashboard para anomalías
   └── /dashboard
       ├── ¿Hay un banner rojo de cuarentena? → revisar y resolver
       └── ¿Active Agents muestra el número correcto?

3. Revisar balances de agentes
   └── /balances → tabla "Agent Budget Allocation"
       ├── Verificar que ningún agente esté al 100% de utilización
       └── Recargar límites si es necesario
```

### Flujo D: Emitir una Tarjeta Virtual para un Agente

```
1. Crear API Key con scope cards:issue
   └── /settings → "Configure New Key"
       └── ⚠ Activar "cards:issue" (CRÍTICO — solo úsalo si es necesario)

2. Ir a la sección de Cards
   └── /cards → "Issue New Card"

3. Configurar la tarjeta
   ├── Asignar límite en USD
   ├── Asignar al agente responsable
   └── Confirmar emisión

4. El agente puede usar la tarjeta para pagos en plataformas externas
   └── Los gastos se descuentan del balance global de la organización
```

---

## 18. Seguridad y Mejores Prácticas

### 18.1 Gestión de Claves API

| ✅ Hacer | ❌ No Hacer |
|---------|------------|
| Guardar claves en variables de entorno (`process.env`) | Hardcodear claves en el código fuente |
| Usar `.env` files con `.gitignore` | Subir claves a repositorios de código (GitHub, GitLab) |
| Crear claves separadas por entorno (test/prod) | Usar la misma clave en desarrollo y producción |
| Revocar claves comprometidas inmediatamente | Ignorar accesos sospechosos en los logs |
| Asignar solo los scopes mínimos necesarios | Dar `cards:issue` a todos los agentes por defecto |

### 18.2 Principio de Mínimo Privilegio (RBAC)

- Un agente que solo necesita **leer** transacciones: solo dale `transactions:read`
- Un agente que necesita **ejecutar** pagos: `transactions:read` + `transactions:write`
- Un agente que necesita **emitir tarjetas**: todos los anteriores + `cards:issue` (con máxima precaución)

### 18.3 Verificación de Webhooks

**Siempre** verifica la firma HMAC-SHA256 de los webhooks recibidos. Un request sin firma válida debe ser rechazado inmediatamente con `HTTP 401`.

### 18.4 Rotación Periódica de Claves

- Rota tus API Keys **cada 90 días** como mínimo
- Tras una rotación: actualiza la clave en todas tus aplicaciones **antes** de revocar la anterior
- En caso de brecha de seguridad: usa "Revoke All API Keys" en Settings → Danger Zone inmediatamente

### 18.5 Monitoreo Continuo

- Revisa los **Watchdog Telemetry Logs** diariamente
- Configura alertas en tu sistema de monitoreo cuando el status no sea `200 OK`
- Presta atención al widget de **Utilization** en `/balances` — si un agente supera el 80%, podría fallar pagos

---

## 19. Glosario

| Término | Definición |
|---------|------------|
| **Agent** | Proceso de software autónomo que puede ejecutar pagos vía API |
| **API Key** | Credencial tipo Bearer Token que identifica y autoriza a un agente |
| **Escrow** | Fondos bloqueados en custodia condicional por un contrato inteligente |
| **KYA** | Know Your Agent — verificación de identidad ZK de un agente |
| **L2 Ledger** | Capa 2 del ledger de TickPay donde se registran todas las transacciones |
| **M2M** | Machine-to-Machine — comunicación directa entre sistemas sin intervención humana |
| **Matching Engine** | Motor que empareja bids y asks del SLA Orderbook automáticamente |
| **Multisig** | Multi-firma — requiere N firmas de M posibles para autorizar una transacción |
| **RBAC** | Role-Based Access Control — control de acceso basado en roles |
| **Scope** | Permiso específico asignado a una API Key |
| **SLA** | Service Level Agreement — acuerdo de nivel de servicio entre agentes |
| **Swarm Wallet** | Wallet compartida por múltiples agentes con governance multifirma |
| **TVL** | Total Value Locked — total de fondos bloqueados en contratos activos |
| **Watchdog** | Sistema de monitoreo de webhooks y telemetría de integraciones |
| **Webhook** | Notificación HTTP que TickPay envía a tu servidor cuando ocurre un evento |
| **HMAC-SHA256** | Algoritmo criptográfico usado para firmar y verificar webhooks |
| **PCI-DSS** | Estándar de seguridad para datos de tarjetas de pago |

---

*Manual generado el 18 de marzo de 2026 · TickPay Platform v1.0*

*Para soporte técnico, visita `/contact` o consulta la documentación en `/docs-intro`*
