using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Grpc.Net.Client;
using GrpcAcronymsClient;

namespace grpc_client.services
{
    internal class AcronymTrainDataServiceService
    {
        private readonly AcronymTrainDataService.AcronymTrainDataServiceClient _client;

        public AcronymTrainDataServiceService()
        {
            var channel = GrpcChannel.ForAddress("http://localhost:50051");
            _client = new AcronymTrainDataService.AcronymTrainDataServiceClient(channel);
        }

        public async Task<AcronymTrainData> create(AcronymTrainData acronym)
        {
            return await _client.createAsync(acronym);
        }

        public async Task<AcronymTrainDataList> get_all()
        {
            return await _client.get_allAsync(new Empty());
        }

        public async Task<AcronymTrainData> update(AcronymTrainData acronym)
        {
            return await _client.updateAsync(acronym);
        }

        public async Task<Empty> delete(AcronymTrainData acronym)
        {
            return await _client.deleteAsync(acronym);
        }

    }
}
