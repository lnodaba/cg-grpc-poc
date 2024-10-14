using GrpcAcronymsClient;
using Grpc.Net.Client;
using System.Threading.Channels;
using System.Runtime;
using Microsoft.Extensions.Options;


namespace TrainingGrpcClient
{
    public class AcronymServiceService
    {
        private readonly AcronymService.AcronymServiceClient _client;
        public AcronymServiceService(String url)
        {
            var channel = GrpcChannel.ForAddress(url);
            _client = new AcronymService.AcronymServiceClient(channel);
        }

        public async Task<Acronym> Create(Acronym acronym)
        {
            
            return await _client.createAsync(acronym);
        }

        public async Task<Acronym> GetById(int id)
        {
            return await _client.get_by_idAsync(new IdRequest { Id = id });
        }

        public async Task<AcronymList> GetAll()
        {

            return await _client.get_allAsync(new Empty());
        }

        public async Task<Acronym> Update(Acronym acronym)
        {
           
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> Delete(Acronym acronym)
        {
           
            return await _client.deleteAsync(acronym);
        }

    }
}
