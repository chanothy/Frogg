const {Client, Events, GatewayIntentBits} = require("discord.js");
const {token} = require("./config.json");


const client = new Client({intents: [GatewayIntentBits.Guilds]});

client.once(Events.ClientReady, readyClient => {
    // readyClient references self
    console.log(`Ready! Logged in as ${readyClient.user.tag}`);
})

client.login(token);
