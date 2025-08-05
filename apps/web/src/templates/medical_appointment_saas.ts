// apps/web/src/templates/medical_appointment_saas.ts
// Definição de um template de projeto para SaaS de agendamento médico.

export const medicalAppointmentSaaS = {
  id: "medical-appointment-saas",
  name: "SaaS de Agendamento Médico",
  description: "Um SaaS completo para agendamento e gerenciamento de consultas médicas.",
  technologies: {
    frontend: "React",
    backend: "FastAPI",
    database: "Supabase",
    auth: "Supabase Auth",
    payments: "Stripe"
  },
  features: [
    "Agendamento de consultas online",
    "Gestão de pacientes",
    "Histórico médico",
    "Notificações por email/SMS",
    "Dashboard administrativo"
  ],
  structure: {
    frontend: [
      "apps/web/src/pages/appointments",
      "apps/web/src/components/forms/AppointmentForm"
    ],
    backend: [
      "services/api-gateway/src/routes/appointments.py",
      "services/api-gateway/src/models/appointment.py"
    ],
    database: [
      "Tabela 'appointments' no Supabase",
      "Tabela 'patients' no Supabase"
    ]
  },
  // Placeholder para a lógica de geração de código real
  generateCode: (projectName: string) => {
    console.log(`Gerando código para o projeto: ${projectName} (SaaS de Agendamento Médico)`);
    // Aqui a lógica real chamaria agentes para gerar os arquivos
    return `Projeto ${projectName} gerado com sucesso!`;
  }
};
