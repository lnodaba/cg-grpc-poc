using Grpc.Net.Client;
using GrpcAcronymsClient;

namespace TrainingGrpcClient
{
    public class TrainsetContentServiceService
    {
        private readonly TrainsetContentService.TrainsetContentServiceClient _client;

        public TrainsetContentServiceService()
        {
            var channel = GrpcChannel.ForAddress("http://localhost:50051");
            _client = new TrainsetContentService.TrainsetContentServiceClient(channel);
        }

        public async Task<TrainsetContent> Create(TrainsetContent acronym)
        {
            return await _client.createAsync(acronym);
        }

        public async Task<TrainsetContent> GetById(int id)
        {
            return await _client.get_by_idAsync(new IdRequest { Id = id });
        }

        public async Task<TrainsetContentList> GetAll()
        {
            return await _client.get_allAsync(new Empty());
        }
        

        public async Task<TrainsetContent> Update(TrainsetContent acronym)
        {
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> Delete(TrainsetContent acronym)
        {
            return await _client.deleteAsync(acronym);
        }
    }
}
