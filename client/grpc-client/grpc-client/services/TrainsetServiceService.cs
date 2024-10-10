using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Grpc.Net.Client;
using GrpcAcronymsClient;

namespace grpc_client.services
{
    internal class TrainsetServiceService
    {
        private readonly TrainsetService.TrainsetServiceClient _client;

        public TrainsetServiceService()
        {
            var channel = GrpcChannel.ForAddress("http://localhost:50051");
            _client = new TrainsetService.TrainsetServiceClient(channel);
        }

        public async Task<Trainset> create(Trainset acronym)
        {
            return await _client.createAsync(acronym);
        }

        public async Task<TrainsetList> get_all()
        {
            return await _client.get_allAsync(new Empty());
        }

        public async Task<Trainset> update(Trainset acronym)
        {
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> delete(Trainset acronym)
        {
            return await _client.deleteAsync(acronym);
        }

    }
}
