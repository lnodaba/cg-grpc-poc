using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using grpc_client.services;
using GrpcAcronymsClient;
using Moq;
using Xunit;

namespace grpc_client.tests;

public class AcronymServiceTest
{
    private readonly services.AcronymServiceService _service;

    public AcronymServiceTest()
    {
        _service = new services.AcronymServiceService();
    }


    [Fact]
    public async Task a_Create()
    {
        // Arrange
        var model = new Acronym
        {
            TextEn = "TermEn",
            TextFr = "TermFr",
            AcronymEn = "acronymEn",
            AcronymFr = "AcronymFr"
        };

        // Act
        var created = await _service.create(model);

        // Assert
        Assert.Equal(model.TextEn, created.TextEn);
        Assert.Equal(model.TextFr, created.TextFr);
        Assert.NotNull(created.CreateDt);
        Assert.NotNull(created.UpdateDt);
    }

    [Fact]
    public async Task b_GetAll()
    {
        // Arrange

        // Act
        var result = await _service.get_all();
        
        // Assert
        Assert.NotNull(result.List);
    }

    [Fact]
    public async Task c_Update()
    {
        // Arrange
        var result = await _service.get_all();
        var last = result.List[result.List.Count - 1];
        last.TextEn = "UpdatedTermEn";
        last.TextFr = "UpdatedTermFr";

        // Act
        var updated = await _service.update(last);

        // Assert
        Assert.Equal(last.TextEn, updated.TextEn);
        Assert.Equal(last.TextFr, updated.TextFr);
        Assert.NotEqual(last.UpdateDt, updated.UpdateDt);
    }

    [Fact]
    public async Task d_Delete()
    {

        // Arrange
        var result = await _service.get_all();
        var last = result.List[result.List.Count - 1];


        // Act
        await _service.delete(last);

        var res = await _service.get_all();

        foreach (var item in res.List)
        {
            Assert.NotEqual(last.Id, item.Id);
        }

    }
}


