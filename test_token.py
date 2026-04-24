import requests 
t="IGAAMZCWWZCehsFBZAGFtLWdibHg0MEZADa09FVkxzaDRWbDdpLUQ2NkZAxeEM4d2VPX2E3NEllT3pDY09uWjJFaWRZAdDRYWWhSbFIwRG1BdWtGMkZAjcHN3VkRCOHNyZAmtqbmdVbnBreXViV1RTeTZADaF9wRkdrVThMaGFwLUp6dTVMQQZDZD" 
r=requests.get("https://graph.facebook.com/v21.0/me?access_token="+t) 
print(r.json()) 
