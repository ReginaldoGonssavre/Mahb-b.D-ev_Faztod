// apps/web/src/pages/pricing.tsx
// Página de preços da plataforma MAHBUB

import React from 'react';

const PricingPage: React.FC = () => {
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl font-bold text-center mb-12">Planos de Assinatura MAHBUB</h1>
      <p className="text-center text-lg mb-8">Escolha o plano que melhor se adapta às suas necessidades de engenharia de software de IA.</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Plano Gratuito */}
        <div className="bg-white rounded-lg shadow-lg p-6 flex flex-col justify-between border-2 border-gray-200">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Gratuito</h2>
            <p className="text-gray-600 mb-4">Ideal para experimentação e projetos pessoais.</p>
            <p className="text-4xl font-bold mb-6">$0<span className="text-lg font-normal">/mês</span></p>
            <ul className="text-gray-700 space-y-2 mb-6">
              <li>✅ Créditos diários limitados para execução de agentes</li>
              <li>✅ Acesso a ferramentas básicas de engenharia de software</li>
              <li>✅ Suporte da comunidade</li>
              <li>❌ Ferramentas avançadas</li>
              <li>❌ Prioridade na fila de execução</li>
            </ul>
          </div>
          <button className="bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition duration-300">Começar Grátis</button>
        </div>

        {/* Plano Developer Pro */}
        <div className="bg-white rounded-lg shadow-lg p-6 flex flex-col justify-between border-2 border-blue-500 transform scale-105">
          <div>
            <h2 className="text-2xl font-semibold text-blue-600 mb-4">Developer Pro</h2>
            <p className="text-gray-600 mb-4">Para desenvolvedores e equipes pequenas que buscam produtividade.</p>
            <p className="text-4xl font-bold mb-6">$XX<span className="text-lg font-normal">/mês</span></p>
            <ul className="text-gray-700 space-y-2 mb-6">
              <li>✅ Créditos diários/mensais aumentados</li>
              <li>✅ Acesso a ferramentas avançadas (Otimização Quântica-Inspirada, Gerador de Firmware)</li>
              <li>✅ Prioridade na fila de execução</li>
              <li>✅ Suporte prioritário</li>
              <li>✅ 10GB de armazenamento para projetos</li>
            </ul>
          </div>
          <button className="bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition duration-300">Assinar Agora</button>
        </div>

        {/* Plano Team Enterprise */}
        <div className="bg-white rounded-lg shadow-lg p-6 flex flex-col justify-between border-2 border-gray-200">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Team Enterprise</h2>
            <p className="text-gray-600 mb-4">Solução completa para grandes equipes e empresas.</p>
            <p className="text-4xl font-bold mb-6">$YY<span className="text-lg font-normal">/mês</span></p>
            <ul className="text-gray-700 space-y-2 mb-6">
              <li>✅ Créditos ilimitados ou pool de créditos grande</li>
              <li>✅ Acesso a recursos de HPC na nuvem</li>
              <li>✅ Agentes dedicados e integrações personalizadas</li>
              <li>✅ Suporte 24/7 e gerente de contas</li>
              <li>✅ SLA garantido</li>
            </ul>
          </div>
          <button className="bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition duration-300">Fale Conosco</button>
        </div>
      </div>

      <p className="text-center text-gray-500 text-sm mt-12">*Os valores de $XX e $YY são placeholders e devem ser definidos com base na sua estratégia de precificação.</p>
    </div>
  );
};

export default PricingPage;
