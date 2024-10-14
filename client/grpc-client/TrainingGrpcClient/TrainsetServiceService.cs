using System;
using Grpc.Net.Client;
using GrpcAcronymsClient;

namespace TrainingGrpcClient
{
    public class TrainsetServiceService
    {
        private readonly TrainsetService.TrainsetServiceClient _client;

        public TrainsetServiceService(String url)
        {
            var channel = GrpcChannel.ForAddress(url);
            _client = new TrainsetService.TrainsetServiceClient(channel);
        }

        public async Task<Trainset> Create(Trainset acronym)
        {
            return await _client.createAsync(acronym);
        }

        public async Task<Trainset> GetById(int id)
        {
            return await _client.get_by_idAsync(new IdRequest { Id = id });
        }

        public async Task<TrainsetList> GetAll()
        {
            return await _client.get_allAsync(new Empty());
        }

        public async Task<Trainset> Update(Trainset acronym)
        {
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> Delete(Trainset acronym)
        {
            return await _client.deleteAsync(acronym);
        }

    }
}
