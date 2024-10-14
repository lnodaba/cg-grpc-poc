using Grpc.Net.Client;
using GrpcAcronymsClient;

namespace TrainingGrpcClient
{
    public class AcronymTrainDataServiceService
    {
        private readonly AcronymTrainDataService.AcronymTrainDataServiceClient _client;

        public AcronymTrainDataServiceService(String url)
        {
            var channel = GrpcChannel.ForAddress(url);
            _client = new AcronymTrainDataService.AcronymTrainDataServiceClient(channel);
        }

        public async Task<AcronymTrainData> Create(AcronymTrainData acronym)
        {
            return await _client.createAsync(acronym);
        }

        public async Task<AcronymTrainData> GetById(int id)
        {
            return await _client.get_by_idAsync(new IdRequest { Id = id });
        }

        public async Task<AcronymTrainDataList> GetAll()
        {
            return await _client.get_allAsync(new Empty());
        }

        public async Task<AcronymTrainData> Update(AcronymTrainData acronym)
        {
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> Delete(AcronymTrainData acronym)
        {
            return await _client.deleteAsync(acronym);
        }

    }
}
