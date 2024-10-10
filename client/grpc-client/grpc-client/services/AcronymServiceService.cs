using GrpcAcronymsClient;
using Grpc.Net.Client;
namespace grpc_client.services
{
    internal class AcronymServiceService
    {
        private readonly AcronymService.AcronymServiceClient _client;

        public AcronymServiceService()
        {
            var channel = GrpcChannel.ForAddress("http://localhost:50051");
            _client = new AcronymService.AcronymServiceClient(channel);
        }

        public async Task<Acronym> create(Acronym acronym)
        {
            return await _client.createAsync(acronym);
        }

        public async Task<AcronymList> get_all()
        {
            return await _client.get_allAsync(new Empty());
        }

        public async Task<Acronym> update(Acronym acronym)
        {
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> delete(Acronym acronym)
        {
            return await _client.deleteAsync(acronym);
        }

    }
}
