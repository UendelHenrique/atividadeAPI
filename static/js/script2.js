
function defineRota(rota) {
    //Redirecionar para a nova rota
    window.location.href = rota;
}

//////////////////////////////////////////////
// Função para mostrar data e hora atual
function mostrarDataHora() {
    const agora = new Date();
    const data = agora.toLocaleDateString("pt-BR");
    const hora = agora.toLocaleTimeString("pt-BR");
    document.getElementById("dataHora").textContent = `Data: ${data} - Hora: ${hora}`;
}


////////////////////////////////////////////////////////////////////////////
// Chamada simples de API
// URL da API para cotação do dólar
const apiUrl = 'https://economia.awesomeapi.com.br/json/last/USD-BRL';

// Função para buscar a cotação
async function fetchExchangeRate() {
    try { //pesquise por que usamos try
        const response = await fetch(apiUrl);
        const data = await response.json();

        // Extrai a cotação do dólar
        const usdToBrl = data.USDBRL.bid;
        console.log(`Cotação do Dólar (USD) para Real (BRL): ${usdToBrl}`);

        // Atualiza apenas o elemento #cotacao, pelo id no html
        const cotacaoElement = document.getElementById('cotacao');
        // o innerHTML substitui
        cotacaoElement.innerHTML = `<p>Cotacao do Dólar: R$ ${usdToBrl}</p>`;

    } catch (error) {
        console.error('Erro ao buscar a cotação:', error);

        // Exibe uma mensagem de erro no elemento #cotacao
        const cotacaoElement = document.getElementById('cotacao');
        cotacaoElement.innerHTML = `<p>Erro ao carregar a cotação.</p>`;
    }
}

// Chama a função
fetchExchangeRate();

////////////////////////////////////////////////////////////////////////////////////////////////
// chamada de API que precisa de argumentos (passagem de valor aos parâmetros)

// chave de API da OpenWeatherMap. Na variável apiKey coloquei a minha e posso desativar
const apiKey = 'fd9ec00118bb6f4d51c88f56edd51400'; //sua_chave_api_aqui';

// Função para buscar a previsão do tempo
async function fetchWeather(cidade) {
    //tem 2 parâmetros (o nome da cidade e a chave para uso da API)
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${cidade}&appid=${apiKey}&units=metric&lang=pt_br`;

    try { //pesquise para que serve try
        const response = await fetch(apiUrl);
        const data = await response.json();

        // Verifica se a cidade foi encontrada (200)
        if (data.cod === 200) {
            // Extrai os dados relevantes
            const nomeCidade = data.name;
            const temperatura = data.main.temp;
            const descriptionTempo = data.weather[0].description;
            const umidade = data.main.humidity;

            // Exibe os dados na página
            const weatherElement = document.getElementById('previsao-tempo');
            // o innerHTML é como inserir esse código html na página. Veja as tags
            weatherElement.innerHTML = `
                <h4>Previsão do Tempo em ${nomeCidade}</h4>
                <p>Temperatura: ${temperatura}°C</p>
                <p>Condição: ${descriptionTempo}</p>
                <p>Umidade: ${umidade}%</p>
            `;
        } else {
            // mensagem de erro se a cidade não for encontrada
            const weatherElement = document.getElementById('previsao-tempo');
            weatherElement.innerHTML = `<p>Cidade não encontrada. Tente novamente.</p>`;
        }
    } catch (error) {
        console.error('Erro ao buscar a previsão do tempo:', error);

        // mensagem de erro no elemento #previsao-tempo
        const weatherElement = document.getElementById('previsao-tempo');
        weatherElement.innerHTML = `<p>Erro ao carregar a previsão do tempo.</p>`;
    }
}

// Chama a função para buscar a previsão do tempo de uma cidade 
//fetchWeather('Curitiba');
//vamos deixar escolher a cidade na tela. Ver base.html

/////////////////////////////////////////////////////////////////////
// Chamada de API criada por nós ?
// deixei em outro arquivo .js --> forms.js