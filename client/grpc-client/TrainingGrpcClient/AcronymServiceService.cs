using GrpcAcronymsClient;
using Grpc.Net.Client;
using System.Threading.Channels;

namespace TrainingGrpcClient
{
    public class AcronymServiceService
    {
        private readonly AcronymService.AcronymServiceClient _client;
        //private readonly GrpcChannel channel;
        public AcronymServiceService()
        {
            var channel = GrpcChannel.ForAddress("http://localhost:50051");
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
